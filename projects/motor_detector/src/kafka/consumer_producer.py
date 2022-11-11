from datetime import datetime
import os
from typing import Tuple

import cv2
import numpy as np

from image_processing_lib import onnx, image_formats
from kafka_lib import producer as kafka_lib_producer
from onnx_lib import model
from mongodb_lib import connection, collection, change
import frames_pb2 as frames_pb

from src.database import motorcycle

KAFKA_HOST = os.environ.get('KAFKA_HOST', default='localhost:9092')
KAFKA_PRODUCER_TOPIC = os.environ.get('KAFKA_PRODUCER_TOPIC', default='motorcycles')
KAFKA_PRODUCER_PARTITIONS = int(os.environ.get('KAFKA_PRODUCER_PARTITIONS', default=1))
MONGO_HOST = os.environ.get('MONGO_HOST', default='localhost')
MONGO_PORT = os.environ.get('MONGO_PORT', default='27017')
MONGO_USER = os.environ.get('MONGO_USER', default='root')
MONGO_PASS = os.environ.get('MONGO_PASS', default='231564')

yolo_v5_onnx_model = model.new_YOLOv5Onnx('./onnx_weights/yolov5m.onnx', 'cpu')
kafka_producer = kafka_lib_producer.create_producer(
    [KAFKA_HOST],
    [KAFKA_PRODUCER_TOPIC],
    KAFKA_PRODUCER_PARTITIONS
)
mongo_connection = connection.create_connection(
    MONGO_HOST,
    MONGO_PORT,
    MONGO_USER,
    MONGO_PASS
)

def update_frame_counter(frame_number):
    frames_counter_coll = collection.access_collection(
        mongo_connection,
        'motor_detection_system',
        'frames_counter'
    )
    frames_counter_coll.update_one(
        { "frame_number": frame_number },
        { "$set": { "end_processing_date": datetime.now() } }
    )

def _serialize_image(data) -> bytes:
    processing_id, motorcycle_id, box, frame, frame_number = data
    message = frames_pb.Motorcycle()
    message.processing_id = str(processing_id)
    message.motorcycle_id = str(motorcycle_id)

    message.frame.frame_number = frame_number
    message.frame.shape.extend(frame.shape)
    png_img = image_formats.matrix_to_png(frame)
    message.frame.frame = png_img

    message.bbox.shape.extend(box.shape)
    message.bbox.box = box.tobytes()

    return message.SerializeToString()

def _send_frame(producer, data):
    message = _serialize_image(data)
    kafka_lib_producer.send_to_producer(producer, message)

def _deserialize_image(data) -> Tuple[bytes, str, int]:
    message = frames_pb.FrameMessage()
    message.ParseFromString(data)

    matrix_img = image_formats.png_to_matrix(message.frame.frame)
    frame = np.frombuffer(matrix_img, dtype=np.uint8)\
        .reshape(message.frame.shape)
    return message.processing_id, message.frame.frame_number, frame

def consume_frames(data):
    print('ok1')
    value = data.value
    processing_id, frame_number, frame = _deserialize_image(value)

    print('ok2')
    onnx_frame = onnx.preprocess_image_to_onnx(frame, True)
    bboxes = model.run_model(yolo_v5_onnx_model, onnx_frame)
    bboxes = np.array(bboxes)

    print('ok3')
    # pros processing to get bounding box
    for box in bboxes:
        [x, y, w, h, confidence, label] = box
        xmin = int(x)
        ymin = int(y)
        xmax = int(w)
        ymax = int(h)

        print('ok4')
        coords = [xmin, ymin, xmax, ymax]
        invalid_coord = any(list(filter(lambda x: x < 0 or x >= 640, coords)))
        if invalid_coord:
            continue
        # send to mongodb
        motorcycles_coll = collection.access_collection(
            mongo_connection,
            'motor_detection_system',
            'motorcycles'
        )
        new_processing = motorcycle.new_motorcycle(
            processing_id,
            frame_number,
            ((xmin, xmax), (ymin, ymax)),
            confidence
        )
        ok, motorcycle_id = change.insert_one(motorcycles_coll, new_processing)
        if not ok:
            continue
        # frame counter
        print('ok5')
        update_frame_counter(frame_number)
        print('ok6')
        # send to kafka
        data = processing_id, motorcycle_id, np.array(coords), frame, frame_number
        _send_frame(kafka_producer, data)
        print('ok7')