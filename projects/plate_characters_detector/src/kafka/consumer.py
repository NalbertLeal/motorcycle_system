from os import environ
from typing import Tuple

import numpy as np
import cv2

from image_processing_lib import image_formats
from kafka_lib import consumer as lib_consumer
import frames_pb2 as frames_pb
from src.nn.recognition import CharactersRecognition
from src.nn.segmentation import CharactersSegmentation

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
    
    chars_positions = positions1 + positions2
    #print(label)
    [plate_1_text, _] = chars_recognition(plate_1, label, positions1, True)
    #print('ok1')
    [plate_2_text, _] = chars_recognition(plate_2, label, positions2, False)
    #print('ok2')
    #print('plate_1_text = ', plate_1_text)
    #print('plate_2_text = ', plate_2_text)

    text = plate_1_text + plate_2_text
    print(text)

    # send recognition result to database