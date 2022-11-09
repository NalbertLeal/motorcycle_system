import os
from typing import Tuple

import numpy as np
import cv2

from image_processing_lib import image_formats
from kafka_lib import consumer as lib_consumer
from kafka_lib import producer as kafka_lib_producer
import frames_pb2 as frames_pb
from src.nn.recognition import CharactersRecognition
from src.nn.segmentation import CharactersSegmentation

KAFKA_HOST = os.environ.get('KAFKA_HOST', default='localhost:9092')
KAFKA_PRODUCER_TOPIC = os.environ.get('KAFKA_PRODUCER_TOPIC', default='plates_text')
KAFKA_PRODUCER_PARTITIONS = int(os.environ.get('KAFKA_PRODUCER_PARTITIONS', default=1))
MONGO_HOST = os.environ.get('MONGO_HOST', default='localhost')
MONGO_PORT = os.environ.get('MONGO_PORT', default='27017')
MONGO_USER = os.environ.get('MONGO_USER', default='root')
MONGO_PASS = os.environ.get('MONGO_PASS', default='231564')

kafka_producer = kafka_lib_producer.create_producer(
    [KAFKA_HOST],
    [KAFKA_PRODUCER_TOPIC],
    KAFKA_PRODUCER_PARTITIONS
)

def _serialize_image(data) -> bytes:
    processing_id, plate_id, box, label, plate_content, frame, frame_number = data
    message = frames_pb.PlateText()
    message.processing_id = str(processing_id)
    message.plate_id = str(plate_id)

    message.frame.frame_number = frame_number
    message.frame.shape.extend(frame.shape)
    png_img = image_formats.matrix_to_png(frame)
    message.frame.frame = png_img

    message.bbox.shape.extend(box.shape)
    message.bbox.box = box.tobytes()
    message.bbox.label = label
    message.bbox.plate_text = plate_content

    return message.SerializeToString()

def _send_frame(producer, data):
    message = _serialize_image(data)
    kafka_lib_producer.send_to_producer(producer, message)

def deserialize(data: bytes) -> Tuple:
    message = frames_pb.Plate()
    message.ParseFromString(data)

    matrix_img = image_formats.png_to_matrix(message.frame.frame)
    frame = np.frombuffer(matrix_img, dtype=np.uint8)\
        .reshape(message.frame.shape)
    bbox = np.frombuffer(message.bbox.box, dtype=np.uint64)\
        .reshape(message.bbox.shape)
    return message.processing_id, message.plate_id,\
        message.frame.frame_number, frame, bbox, message.bbox.label

def plate_img_segmentation(plate_img):
    # gray binarization
    gray_img = cv2.cvtColor(plate_img, cv2.COLOR_BGR2GRAY)
    gray_img = cv2.cvtColor(gray_img, cv2.COLOR_GRAY2RGB)
    _, bin_img = cv2.threshold(gray_img, 127, 255, cv2.THRESH_BINARY)

    # divide img
    (h, w, _) = bin_img.shape
    plate_1 = np.copy(bin_img[:h//2])
    plate_2 = np.copy(bin_img[h//2:])

    # segmentation
    seg = CharactersSegmentation()
    (positions1, seg_conf1) = seg.run(plate_1)
    seg = CharactersSegmentation()
    (positions2, seg_conf2) = seg.run(plate_2)

    return plate_1, positions1, seg_conf1, plate_2, positions2, seg_conf2

def chars_recognition(plate_img, label, positions, is_fst_half):
    rec = CharactersRecognition()
    (plate_text, plate_confidence) = rec.recognition(
        plate_img,
        label,
        positions,
        is_fst_half
    )
    return plate_text

def receive_image(data: bytes):
    processing_id, plate_id, frame_number, frame, bbox, label = deserialize(data.value)
    
    # crop frame
    [x, y, w, h] = bbox
    motorcycle_frame = frame[y:h, x:w]
    
    plate_1, positions1, seg_conf1, plate_2, positions2, seg_conf2 = plate_img_segmentation(motorcycle_frame)
    
    if positions1 == [] or positions2 == []:
        return
    [plate_1_text, _] = chars_recognition(plate_1, label, positions1, True)
    [plate_2_text, _] = chars_recognition(plate_2, label, positions2, False)

    plate_content = plate_1_text + '-' + plate_2_text
    print(plate_content)

    data = processing_id, plate_id, bbox, label, plate_content, frame, frame_number
    _send_frame(kafka_producer, data)

    # send recognition result to database