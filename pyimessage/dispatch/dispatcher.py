from multiprocessing import Queue
import queue
import json
import threading
import time

from pyimessage.notifications.receiver import NotificationReceiver
from pyimessage.imessage.client import iMessageClient
from config import Config


MESSAGE_QUEUE_NAME = Config.imessage_queue_name
IMESSAGE_DB = Config.imessage_db_location


class MessageReceiver(threading.Thread):
    def __init__(self, task_queue):
        super(MessageReceiver, self).__init__()
        self.receiver = NotificationReceiver(MESSAGE_QUEUE_NAME)
        self.task_queue = task_queue

        self._stop = threading.Event()
        self.start()

    def run(self):

        notifications = self.receiver.get_notifications()

        for notification in notifications:
            if self.stopped():
                notifications.send(False)
                break

            print("Processed message")
            self.task_queue.put(notification)
            notifications.send(True)

    def stop(self):
        self._stop.set()

    def stopped(self):
        return self._stop.isSet()


class MessageDispatcher(threading.Thread):
    def __init__(self, queue, batch_size=10, batch_delay=3.0, max_batches=float('inf')):
        super(MessageDispatcher, self).__init__()
        self.imessage_client = iMessageClient(IMESSAGE_DB)
        self.queue = queue
        self.batch_size = batch_size
        self.batch_delay = batch_delay
        self.max_batches = max_batches
        self.queue_timeout = 0.05
        self.batches_completed = 0
        self.current_batch = []

        self.daemon = True
        self.start()

    def run(self):
        while True:
            if self.batches_completed >= self.max_batches:
                break

            if len(self.current_batch) >= self.batch_size:
                self._dispatch_batch()
                self.current_batch = []
                self.batches_completed += 1
                time.sleep(self.batch_delay)

                continue

            try:
                message = self.queue.get(True, self.queue_timeout)
            except queue.Empty:
                continue

            print("Received message")
            decoded_message = json.loads(message)
            message_body = json.loads(decoded_message['Message'])
            phone_number = message_body['phone_number']
            text = message_body['text']

            self.current_batch.append((phone_number, text))

    def _dispatch_batch(self):
        for phone_number, text in self.current_batch:
            self._dispatch_message(phone_number=phone_number, text=text)

    def _dispatch_message(self, phone_number, text):
        self.imessage_client.send_imessage(phone_number=phone_number, text=text)

    def dispatch_sms(self, phone_number, text):
        pass
