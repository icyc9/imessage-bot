import sqlite3


IMESSAGE_DB = '/Users/rob/Library/Messages/chat.db'


conn = sqlite3.connect(IMESSAGE_DB)

def get_failed_imessages():
    c = conn.cursor() 
    messages = c.execute('select is_delivered, text from message')

    for message in messages:
        if not message[0]:
            yield message
