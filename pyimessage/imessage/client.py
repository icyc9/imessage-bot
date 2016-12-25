import sqlite3
import os

import applescript


SCRIPT_PATH = os.path.join(os.path.dirname(
	os.path.dirname(__file__)), 'applescript/imessage.applescript')


class iMessageClient(object):
	def __init__(self, sql_db):
		self.conn = sqlite3.connect(sql_db)
		self.script_src = open(SCRIPT_PATH).read()
		self.script = applescript.AppleScript(source=self.script_src)

	def get_failed_messages(self):
		c = self.conn.cursor() 
		messages = c.execute('select ROWID, is_sent, text from message')

		for message in messages:
			if not message[1]:
				yield message

	def remove_message(self, message_row_id):
		c = self.conn.cursor()
		c.execute('DELETE FROM message WHERE ROWID=?', (message_row_id,))
		self.conn.commit()

	def send_imessage(self, phone_number, text):
		self.script.call('send_imessage', phone_number, text)