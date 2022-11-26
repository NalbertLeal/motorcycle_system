import sys
sys.path.append('../../libs/mongodb_lib')

import argparse
import csv
import os

import pymongo

from mongodb_lib import connection, collection

# CONSTANTS

MONGO_HOST = os.environ.get('MONGO_HOST', default='localhost')
MONGO_PORT = os.environ.get('MONGO_PORT', default='27017')
MONGO_USER = os.environ.get('MONGO_USER', default='root')
MONGO_PASS = os.environ.get('MONGO_PASS', default='231564')

# CMD ARGS

parser = argparse.ArgumentParser(description='Send media file (video) to the backend identify motorcycles.')
parser.add_argument('--name', type=str, required=True)
args = parser.parse_args()

# FUNCTIONS

def save_into_csv(dict_list, file_name):
    keys = dict_list[0].keys()

    with open(f'{file_name}.csv', 'w', newline='') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(dict_list)

# CONNECTION

mongo_connection = connection.create_connection(
    MONGO_HOST,
    MONGO_PORT,
    MONGO_USER,
    MONGO_PASS
)

# COLLECTIONS

frames_counter_coll = collection.access_collection(
  mongo_connection,
  'motor_detection_system',
  'frames_counter'
)
motor_metrics_coll = collection.access_collection(
  mongo_connection,
  'motor_detection_system',
  'motor_metrics'
)
plate_metrics_coll = collection.access_collection(
  mongo_connection,
  'motor_detection_system',
  'plate_metrics'
)
plate_content_metrics_coll = collection.access_collection(
  mongo_connection,
  'motor_detection_system',
  'plate_content_metrics'
)

# CALCULATE THE totsl TEST TIME

first_processed_frame = frames_counter_coll.find({}).sort([
  ('end_processing_date', pymongo.ASCENDING),
]).limit(1)
first_processed_frame = list(first_processed_frame)[0]

last_processed_frame = frames_counter_coll.find({}).sort([
  ('end_processing_date', pymongo.DESCENDING),
]).limit(1)
last_processed_frame = list(last_processed_frame)[0]

total_test_time = last_processed_frame['end_processing_date'] - first_processed_frame['end_processing_date']
with open(f'{args.name}_total_time_to_finish.txt', 'w') as f:
    f.write(str(total_test_time))

motor_metrics = motor_metrics_coll.find({})
motor_metrics = list(motor_metrics)
save_into_csv(motor_metrics, f'{args.name}_motor_metrics')

plate_metrics = plate_metrics_coll.find({})
plate_metrics = list(plate_metrics)
save_into_csv(plate_metrics, f'{args.name}_plate_metrics')

plate_content_metrics = plate_content_metrics_coll.find({})
plate_content_metrics = list(plate_content_metrics)
save_into_csv(plate_content_metrics, f'{args.name}_plate_content_metrics')