from datetime import datetime
import os
from typing import Tuple

import numpy as np
import cv2

from image_processing_lib import image_formats
from kafka_lib import consumer as lib_consumer
from kafka_lib import producer as kafka_lib_producer
from mongodb_lib import connection, collection, change
import frames_pb2 as frames_pb
from src.nn.recognition import CharactersRecognition
from src.nn.segmentation import CharactersSegmentation
from src.database import new_plate_content

# kafka
KAFKA_HOST = os.environ.get('KAFKA_HOST', default='localhost:9092')
KAFKA_PRODUCER_TOPIC = os.environ.get('KAFKA_PRODUCER_TOPIC', default='plates_text')
KAFKA_PRODUCER_PARTITIONS = int(os.environ.get('KAFKA_PRODUCER_PARTITIONS', default=1))
# model
MONGO_HOST = os.environ.get('MONGO_HOST', default='localhost')
MONGO_PORT = os.environ.get('MONGO_PORT', default='27017')
MONGO_USER = os.environ.get('MONGO_USER', default='root')
MONGO_PASS = os.environ.get('MONGO_PASS', default='231564')
# Model
USE_GPU = int(os.environ.get('USE_GPU', default='0'))
# Segmentation model
SEGMENTATION_CFG = './nn_weights/segmentation/yolov4-tiny-ufpr-ufrnv178-prf-224x64_v9.cfg'
SEGMENTATION_WEIGHTS = './nn_weights/segmentation/yolov4-tiny-ufpr-ufrnv178-prf-224x64_best_v9.weights'
# Recognition Letter - Brasil
class_old_lett_cfg = "./nn_weights/recognition/9_gabo_oldLet.cfg"
class_old_lett_wei = "./nn_weights/recognition/9_gabo_oldLet_80000.weights"
# Recognition Number - Brasil
class_old_numb_cfg = "./nn_weights/recognition/3_gabo_oldNum.cfg"
class_old_numb_wei = "./nn_weights/recognition/3_gabo_oldNum.weights" #100000
# Recognition Letter - mercosul
class_new_lett_cfg = "./nn_weights/recognition/3_gabo_newLet.cfg"
class_new_lett_wei = "./nn_weights/recognition/3_gabo_newLet_40000.weights"
# Recognition Number - mercosul
class_new_numb_cfg = "./nn_weights/recognition/2_gabo_newNum.cfg"
class_new_numb_wei = "./nn_weights/recognition/2_gabo_newNum_60000.weights"  

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

# Segment network
seg_net = cv2.dnn.readNetFromDarknet(SEGMENTATION_CFG, SEGMENTATION_WEIGHTS)
seg_net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
seg_net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA_FP16)

# Brazil letter recoognition
class_old_lett = cv2.dnn.readNetFromDarknet(class_old_lett_cfg, class_old_lett_wei)
class_old_lett.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
class_old_lett.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA_FP16)

# Brazil number recoognition
class_old_numb = cv2.dnn.readNetFromDarknet(class_old_numb_cfg, class_old_numb_wei)
class_old_numb.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
class_old_numb.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA_FP16)

# Mercosul letter recoognition
class_new_lett = cv2.dnn.readNetFromDarknet(class_new_lett_cfg, class_new_lett_wei)
class_new_lett.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
class_new_lett.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA_FP16)

# Mercosul number recoognition
class_new_numb = cv2.dnn.readNetFromDarknet(class_new_numb_cfg, class_new_numb_wei)
class_new_numb.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
class_new_numb.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA_FP16)

def update_frame_counter(frame_number):
    # print(frame_number)
    frames_counter_coll = collection.access_collection(
        mongo_connection,
        'motor_detection_system',
        'frames_counter'
    )
    frames_counter_coll.update_one(
        {"frame_number": frame_number},
        {"$set": { "end_processing_date": datetime.now() } }
    )
    # print(frame_number)

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

    seg = CharactersSegmentation(seg_net)
    (positions1, seg_conf1) = seg.run(plate_1)
    seg = CharactersSegmentation(seg_net)
    (positions2, seg_conf2) = seg.run(plate_2)

    return plate_1, positions1, seg_conf1, plate_2, positions2, seg_conf2

def chars_recognition(plate_img, label, positions, is_fst_half):
    rec = CharactersRecognition(class_old_lett, class_old_numb, class_new_lett, class_new_numb)
    (plate_text, plate_confidence) = rec.recognition(
        plate_img,
        label,
        positions,
        is_fst_half
    )
    if len(plate_text) == 0:
        return ''
    return plate_text[0]

def save_at_mongodb(
        processing_id,
        plate_id,
        frame_number,
        content
    ):
    plates_content_coll = collection.access_collection(
        mongo_connection,
        'motor_detection_system',
        'plates_content'
    )
    plate_content_dict = new_plate_content.new_plate_content(
        processing_id,
        plate_id,
        frame_number,
        content
    )
    ok, mongo_id = change.insert_one(plates_content_coll, plate_content_dict)
    if not ok:
        return None
    return mongo_id

def receive_image(data: bytes):
    processing_id, plate_id, frame_number, frame, bbox, label = deserialize(data.value)
    
    # crop frame
    [x, y, w, h] = bbox
    motorcycle_frame = frame[y:h, x:w]
    
    plate_1, positions1, seg_conf1, plate_2, positions2, seg_conf2 = plate_img_segmentation(motorcycle_frame)
    
    if positions1 == [] or positions2 == []:
        return
    plate_1_text = chars_recognition(plate_1, label, positions1, True)

    plate_2_text = chars_recognition(plate_2, label, positions2, False)

    plate_content = plate_1_text + '-' + plate_2_text
    # print(plate_content)

    # save result in mongodb
    save_at_mongodb(processing_id, plate_id, frame_number, plate_content)
    # frame counter
    update_frame_counter(frame_number)

    data = processing_id, plate_id, bbox, label, plate_content, frame, frame_number
    _send_frame(kafka_producer, data)