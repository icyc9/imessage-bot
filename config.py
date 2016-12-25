import os


class Config(object):
    aws = {
      'access_key_id': os.environ['AWS_ACCESS_KEY_ID'],
      'secret_access_key': os.environ['AWS_SECRET_ACCESS_KEY'],
      'region_name': os.environ['AWS_DEFAULT_REGION'],
    }

    imessage_queue_name = os.environ['IMESSSAGE_QUEUE_NAME']
    imessage_db_location = os.environ['IMESSAGE_DB_LOCATION']