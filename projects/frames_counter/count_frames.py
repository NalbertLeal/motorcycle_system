import sys
sys.path.append('../../libs/mongodb_lib')

import os

import pymongo

from kafka_lib import consumer as kafka_lib_consumer
from mongodb_lib import connection, collection

MONGO_HOST = os.environ.get('MONGO_HOST', default='localhost')
MONGO_PORT = os.environ.get('MONGO_PORT', default='27017')
MONGO_USER = os.environ.get('MONGO_USER', default='root')
MONGO_PASS = os.environ.get('MONGO_PASS', default='231564')

mongo_connection = connection.create_connection(
    MONGO_HOST,
    MONGO_PORT,
    MONGO_USER,
    MONGO_PASS
)

frames_counter_coll = collection.access_collection(
    mongo_connection,
    'motor_detection_system',
    'frames_collection'
)

all_dates = frames_counter_coll.find(...).sort([
  ('end_processing_date', pymongo.ASCENDING),
])

result = all_dates[1] - all_dates[0]
print(result)