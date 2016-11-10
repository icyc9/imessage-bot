import json
from datetime import datetime
import boto3


def setup_sns_client():
    return boto3.client('sns')


def setup_sns_resource():
    return boto3.resource('sns')


class NotificationSender:
    def __init__(self, topic):
        self.sns_client = setup_sns_client()
        self.sns_resource = setup_sns_resource()
        self.topic = self.sns_resource.create_topic(Name=topic)
        self.topic_arn = self.topic.arn

    def send(self, message):
        base_message = create_message_base()
        message_body = {**message, **base_message}

        self.sns_client.publish(TopicArn=self.topic_arn,
                                Message=json.dumps(message_body))


def create_message_base():
    timestamp = datetime.utcnow()
    datetime_str = '{}Z'.format(timestamp.isoformat())
    base_message = {'source': 'finegar', 'timestamp_sent': datetime_str}
    return base_message