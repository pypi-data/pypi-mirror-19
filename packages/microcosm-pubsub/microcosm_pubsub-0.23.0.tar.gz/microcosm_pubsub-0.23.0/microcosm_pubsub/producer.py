"""
Message producer.

"""
from collections import defaultdict

from boto3 import client
from microcosm.api import defaults
from microcosm.errors import NotBoundError
from microcosm_logging.decorators import logger
from microcosm_logging.timing import elapsed_time

from microcosm_pubsub.errors import TopicNotDefinedError


@logger
class SNSProducer(object):
    """
    Produces messages to SNS topics.

    """
    def __init__(self, opaque, pubsub_message_schema_registry, sns_client, sns_topic_arns):
        self.opaque = opaque
        self.pubsub_message_schema_registry = pubsub_message_schema_registry
        self.sns_client = sns_client
        self.sns_topic_arns = sns_topic_arns

    def produce(self, media_type, dct=None, **kwargs):
        """
        Produce a message.

        :returns: the message id

        """
        message, topic_arn, opaque_data = self.create_message(media_type, dct, **kwargs)
        return self.publish_message(media_type, message, topic_arn, opaque_data)

    def create_message(self, media_type, dct, opaque_data=None, **kwargs):
        if opaque_data is None:
            opaque_data = dict()

        if self.opaque is not None:
            opaque_data.update(self.opaque.as_dict())

        topic_arn = self.choose_topic_arn(media_type)
        message = self.pubsub_message_schema_registry[media_type].encode(
            dct,
            opaque_data=opaque_data,
            **kwargs
        )
        return message, topic_arn, opaque_data

    def publish_message(self, media_type, message, topic_arn, opaque_data):
        extra = dict(
            media_type=media_type,
            **opaque_data
        )
        self.logger.debug("Publishing message with media type {media_type}", extra=extra)

        with elapsed_time(extra):
            result = self.sns_client.publish(
                TopicArn=topic_arn,
                Message=message,
            )

        self.logger.info("Published message with media type {media_type}", extra=extra)

        return result["MessageId"]

    def choose_topic_arn(self, media_type):
        """
        Choose a topic for this type of message.

        """
        try:
            topic_arn = self.sns_topic_arns[media_type]
        except KeyError:
            topic_arn = None

        if topic_arn is None:
            raise TopicNotDefinedError("No topic arn was registered for messages of type: {}".format(
                media_type,
            ))
        return topic_arn


class DeferredProducer(object):
    """
    A context manager to defer message production until the end of a block.

    """
    def __init__(self, producer):
        self.producer = producer
        self.messages = []

    def produce(self, media_type, dct=None, **kwargs):
        message, topic_arn, opaque_data = self.producer.create_message(media_type, dct, **kwargs)
        self.messages.append((media_type, message, topic_arn, opaque_data))

    def __enter__(self):
        self.message = []
        return self

    def __exit__(self, type, value, traceback):
        if type is not None:
            return

        for media_type, message, topic_arn, opaque_data in self.messages:
            self.producer.publish_message(media_type, message, topic_arn, opaque_data)


@defaults(
    default=None,
    mappings={},
)
def configure_sns_topic_arns(graph):
    """
    Configure a mapping from message types to topic ARNs.

    """
    if graph.config.sns_topic_arns.default is None:
        sns_topic_arns = dict()
    else:
        sns_topic_arns = defaultdict(lambda: graph.config.sns_topic_arns.default)

    sns_topic_arns.update(graph.config.sns_topic_arns.mappings)

    return sns_topic_arns


def configure_sns_producer(graph):
    """
    Configure an SNS producer.

    The SNS Producer requires the following collaborators:
        - Opaque from microcosm.opaque for capturing context information
        - an aws sns client, i.e. from boto.
        - pubsub message codecs: see tests for examples.
        - sns topic arns: see tests for examples.

    """
    if graph.metadata.testing:
        from mock import MagicMock
        sns_client = MagicMock()
    else:
        sns_client = client("sns")

    try:
        opaque = graph.opaque
    except NotBoundError:
        opaque = None

    return SNSProducer(
        opaque=opaque,
        pubsub_message_schema_registry=graph.pubsub_message_schema_registry,
        sns_client=sns_client,
        sns_topic_arns=graph.sns_topic_arns,
    )
