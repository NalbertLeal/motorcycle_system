from datetime import datetime
import os
from typing import Tuple

import cv2
import numpy as np

from image_processing_lib import onnx, image_matrix, image_formats
from kafka_lib import producer as kafka_lib_producer
from onnx_lib import model
from mongodb_lib import connection, collection, change
import frames_pb2 as frames_pb

from src.database import motorcycle_plate

# kafka envs
KAFKA_HOST = os.environ.get('KAFKA_HOST', default='localhost:9092')
KAFKA_PRODUCER_TOPIC = os.environ.get('KAFKA_PRODUCER_TOPIC', default='plates')
KAFKA_PRODUCER_PARTITIONS = int(os.environ.get('KAFKA_PRODUCER_PARTITIONS', default=1))
# mongo envs
MONGO_HOST = os.environ.get('MONGO_HOST', default='localhost')
MONGO_PORT = os.environ.get('MONGO_PORT', default='27017')
MONGO_USER = os.environ.get('MONGO_USER', default='root')
MONGO_PASS = os.environ.get('MONGO_PASS', default='231564')
# model envs
YOLOv5_IMAGE_HEIGHT = 640
YOLOv5_IMAGE_WIDTH = 640
MODEL_PATH = os.environ.get('MODEL_PATH', default='./onnx_weights/yolov5m_v4.onnx')
CPU_GPU = os.environ.get('CPU_GPU', default='cpu')
MODEL_IS_FP16 = bool(os.environ.get('MODEL_IS_FP16', default=0))

yolo_v5_onnx_model = model.new_YOLOv5Onnx(MODEL_PATH, CPU_GPU)
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
    processing_id, plate_id, box, label, frame, frame_number = data
    message = frames_pb.Plate()
    message.processing_id = str(processing_id)
    message.plate_id = str(plate_id)

    message.frame.frame_number = frame_number
    message.frame.shape.extend(frame.shape)
    png_img = image_formats.matrix_to_png(frame)
    message.frame.frame = png_img

    message.bbox.shape.extend(box.shape)
    message.bbox.box = box.tobytes()
    message.bbox.label = label

    return message.SerializeToString()

def _send_frame(producer, data):
    message = _serialize_image(data)
    kafka_lib_producer.send_to_producer(producer, message)

def _deserialize_image(data) -> Tuple[bytes, str, int]:
    message = frames_pb.Motorcycle()
    message.ParseFromString(data)

    matrix_img = image_formats.png_to_matrix(message.frame.frame)
    frame = np.frombuffer(matrix_img, dtype=np.uint8)\
        .reshape(message.frame.shape)
    bbox = np.frombuffer(message.bbox.box, dtype=np.uint64)\
        .reshape(message.bbox.shape)
    return message.processing_id, message.motorcycle_id,\
        message.frame.frame_number, frame, bbox

def destruct_bbox(box):
    [x, y, w, h, confidence, label] = box
    xmin = int(x)
    ymin = int(y)
    xmax = int(w)
    ymax = int(h)
    return (xmin, ymin, xmax, ymax), confidence, label

def is_not_valid_frame_coords(coords):
    return any(list(filter(lambda x: x < 0 or x >= 640, coords)))

def save_at_mongodb(
        processing_id,
        motorcycle_id,
        frame_number,
        coords,
        confidence,
        label
    ):
    x, y, w, h = coords
    motorcycles_plates_coll = collection.access_collection(
        mongo_connection,
        'motor_detection_system',
        'motorcycles_plates'
    )
    motorcycle_plate_dict = motorcycle_plate.new_motorcycle_plate(
        processing_id,
        motorcycle_id,
        frame_number,
        ((x, w), (y, h)),
        confidence,
        label
    )
    ok, plate_id = change.insert_one(motorcycles_plates_coll, motorcycle_plate_dict)
    if not ok:
        # raise BaseException(
        #     'Error while saving into database frame ' + str(frame_number)
        # )
        return None
    return plate_id

def label_to_string(label):
    int_label = int(label)
    if int_label == 0:
        return 'brasil'
    elif int_label == 1:
        return 'light'
    return 'mercosul'

def consume_frames(data):
    value = data.value
    processing_id, motorcycle_id, frame_number,\
        frame, motor_bbox = _deserialize_image(value)
        
    # crop motorcycle from the frame
    [x, y, w, h] = motor_bbox
    resized_frame = image_matrix.resizeAndPad(frame)
    motorcycle_frame = resized_frame[y:h, x:w]

    model_fp = None
    if MODEL_IS_FP16:
        model_fp = np.float16
    else:
        model_fp = np.float32

    # inference
    onnx_frame = onnx.preprocess_image_to_onnx(motorcycle_frame, True, model_fp)
    bboxes = model.run_model(yolo_v5_onnx_model, onnx_frame)
    bboxes = np.array(bboxes)

    # pros processing to get bounding box
    for box in bboxes:
        coords, confidence, label = destruct_bbox(box)
        str_label = label_to_string(label)
        if str_label == 'light':
            continue
        if is_not_valid_frame_coords(coords):
            continue

        plate_id = save_at_mongodb(
            processing_id,
            motorcycle_id,
            frame_number,
            coords,
            confidence,
            label
        )
        if plate_id is None:
            continue
        # frame counter
        update_frame_counter(frame_number)
        # frame resize
        resized_frame = image_matrix.resizeAndPad(motorcycle_frame)
        data = processing_id, plate_id, np.array(coords), str_label,\
            resized_frame, frame_number
        _send_frame(kafka_producer, data)
        # [x, y, w, h, confidence, label] = box
        # xmin = int(x)
        # ymin = int(y)
        # xmax = int(w)
        # ymax = int(h)

        # coords = [xmin, ymin, xmax, ymax]
        # invalid_coord = any(list(filter(lambda x: x < 0 or x >= 640, coords)))
        # if invalid_coord:
        #     break
        # # send to mongodb
        # motorcycles_plates_coll = collection.access_collection(
        #     mongo_connection,
        #     'motor_detection_system',
        #     'motorcycles_plates'
        # )
        # motorcycle_plate_dict = motorcycle_plate.new_motorcycle_plate(
        #     processing_id,
        #     motorcycle_id,
        #     frame_number,
        #     ((xmin, xmax), (ymin, ymax)),
        #     confidence
        # )
        # ok, plate_id = change.insert_one(motorcycles_plates_coll, motorcycle_plate_dict)
        # if not ok:
        #     raise BaseException(
        #         'Error while saving into database frame ' + str(frame_number)
        #     )
        # # send to kafka
        # data = processing_id, plate_id, np.array(coords), frame, frame_number
        # _send_frame(kafka_producer, data)