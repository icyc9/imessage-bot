from time import sleep
import boto3


class NotificationReceiver:

    MESSAGE_KEY = 'Messages'

    def __init__(self, queue_name):
        self.sqs_client = boto3.client('sqs')
        response = self.sqs_client.get_queue_url(QueueName=queue_name)
        self.url = response['QueueUrl']

    def get_notifications(self, max_attempts=float('inf'), timeout=0):

        attempts = 0

        while True:
            response = self.sqs_client.receive_message(QueueUrl=self.url)

            if self.MESSAGE_KEY not in response:
                continue

            message = response[self.MESSAGE_KEY][0]

            # halt control until outside message is processed.
            yield message['Body']

            receipt_handle = message['ReceiptHandle']

            self.sqs_client.delete_message(QueueUrl=self.url,
                                           ReceiptHandle=receipt_handle)

            if attempts < max_attempts:
                attempts += 1
            else:
                break

            sleep(timeout)