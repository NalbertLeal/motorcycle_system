from datetime import datetime
import os
from threading import Thread
import time

import cv2

from mongodb_lib import connection, collection, change
from kafka_lib import producer as kafka_lib_producer
from image_processing_lib import image_formats
import frame_pb2 as frame_pb

from src.utils import file

KAFKA_HOST = os.environ.get('KAFKA_HOST', default='localhost:9092')
MONGO_HOST = os.environ.get('MONGO_HOST', default='localhost')
MONGO_PORT = os.environ.get('MONGO_PORT', default='27017')
MONGO_USER = os.environ.get('MONGO_USER', default='root')
MONGO_PASS = os.environ.get('MONGO_PASS', default='231564')

CONN = connection.create_connection(
    MONGO_HOST,
    MONGO_PORT,
    MONGO_USER,
    MONGO_PASS
)

def create_frame_counter(frame_number):
    frames_counter_coll = collection.access_collection(
        CONN,
        'motor_detection_system',
        'frames_counter'
    )
    new_frame = {
        'frame_number': frame_number,
        'start_processing_date': datetime.now(),
        'end_processing_date': datetime.now(),
    }
    change.insert_one(frames_counter_coll, new_frame)

def _serialize_image(data) -> bytes:
    processing_id, frame, frame_number = data
    message = frame_pb.FrameMessage()

    message.processing_id = str(processing_id)
    
    message.frame.frame_number = frame_number
    message.frame.shape.extend(frame.shape)
    png_img = image_formats.matrix_to_png(frame)
    message.frame.frame = png_img
    
    return message.SerializeToString()

def _send_frame(producer, data):
    message = _serialize_image(data)
    kafka_lib_producer.send_to_producer(producer, message)

def _thread_send_video(file_path: str, processing_id: str):
    kafka_producer = kafka_lib_producer.create_producer(
        [KAFKA_HOST],
        ['media_read'],
        1
    )
    video_reader = file.read_video_frames(file_path)
    video_data = next(video_reader)
    while video_data is not None:
        video_data = next(video_reader)
        if video_data is None:
            return
        (frame, frame_counter, _) = video_data
        data = processing_id, frame, frame_counter
        _send_frame(kafka_producer, data)
        create_frame_counter(frame_counter)

def send_video(file_path: str, processing_id: str):
    t = Thread(target=_thread_send_video, args=[file_path, processing_id])
    t.start()

def send_image(file_path, processing_id):
    frame = cv2.imread(file_path, cv2.IMREAD_COLOR)
    #print('frame line 50: ', frame.shape)
    data = processing_id, frame, 1
    kafka_producer = kafka_lib_producer.create_producer(
        [KAFKA_HOST],
        ['media_read'],
        1
    )
    _send_frame(kafka_producer, data)