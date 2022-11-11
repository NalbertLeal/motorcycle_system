import sys
sys.path.append('../../libs/mongodb_lib')

import os

import pymongo

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
  'frames_counter'
)

sorted_by_start = frames_counter_coll.find({}).sort([
  ('end_processing_date', pymongo.ASCENDING),
])
sorted_by_start = list(sorted_by_start)

sorted_by_end = frames_counter_coll.find({}).sort([
  ('start_processing_date', pymongo.DESCENDING),
])
sorted_by_end = list(sorted_by_end)

procesing_start = sorted_by_start[0]
procesing_end = sorted_by_end[0]

print(procesing_start)
print('')
print(procesing_end)

result = procesing_end - procesing_start
print(result)