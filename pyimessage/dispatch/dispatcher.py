import json
import threading
from multiprocessing import Queue

from pyimessage.notifications.receiver import NotificationReceiver
from pyimessage.imessage.client import iMessageClient
from config import Config


MESSAGE_QUEUE_NAME = Config.imessage_queue_name
IMESSAGE_DB = Config.imessage_db_location


class MessageReceiver(object):
    def __init__(self, queue):
        self.receiver = NotificationReceiver(MESSAGE_QUEUE_NAME)
        self.queue = queue

        thread = threading.Thread(target=self.run, args=())
        thread.daemon = True
        thread.start()

    def run(self):
        notifications = self.receiver.get_notifications()

        for notification in notifications:
            self.queue.put(notification)


class MessageDispatcher(object):
    def __init__(self, queue):
        self.imessage_client = iMessageClient(IMESSAGE_DB)
        self.queue = queue

        thread = threading.Thread(target=self.run, args=())
        thread.daemon = True
        thread.start()

    def run(self):
        while True:
            message = self.queue.get(block=True)
            decoded_message = json.loads(message)
            phone_number = decoded_message['phone_number']
            text = decoded_message['text']

            print("Dispatched message: %s" % phone_number)
            self._dispatch_message(phone_number, text)

    def _dispatch_message(self, phone_number, text):
        self.imessage_client.send_imessage(phone_number=phone_number, text=text)

