import os
from typing import Tuple

import cv2
import numpy as np

from image_processing_lib import image_matrix, image_formats
from kafka_lib import producer as kafka_lib_producer
import frames_pb2 as frames_pb

# # plate text
def _deserialize_image(data) -> Tuple[bytes, str, int]:
    message = frames_pb.PlateText()
    message.ParseFromString(data)

    matrix_img = image_formats.png_to_matrix(message.frame.frame)
    frame = np.frombuffer(matrix_img, dtype=np.uint8)\
        .reshape(message.frame.shape)
    bbox = np.frombuffer(message.bbox.box, dtype=np.int64)\
        .reshape(message.bbox.shape)
    print(message.bbox.label)
    return bbox, message.frame.frame_number, frame, message.bbox.label, message.bbox.plate_text

# # Plate
# def _deserialize_image(data) -> Tuple[bytes, str, int]:
#     message = frames_pb.Plate()
#     message.ParseFromString(data)
# 
#     matrix_img = image_formats.png_to_matrix(message.frame.frame)
#     frame = np.frombuffer(matrix_img, dtype=np.uint8)\
#         .reshape(message.frame.shape)
#     bbox = np.frombuffer(message.bbox.box, dtype=np.int64)\
#         .reshape(message.bbox.shape)
#     return bbox, message.bbox.label, message.frame.frame_number, frame

# motorcycles
# def _deserialize_image(data) -> Tuple[bytes, str, int]:
#     message = frames_pb.Motorcycle()
#     message.ParseFromString(data)

#     matrix_img = image_formats.png_to_matrix(message.frame.frame)
#     frame = np.frombuffer(matrix_img, dtype=np.uint8)\
#         .reshape(message.frame.shape)
#     bbox = np.frombuffer(message.bbox.box, dtype=np.uint64)\
#         .reshape(message.bbox.shape)
#     return message.processing_id, message.motorcycle_id,\
#         message.frame.frame_number, frame, bbox

im_path = '/home/nalbertgml/Documentos/motor-plates-detection-monorepo/projects/visualizer/frames/frame_'
def consume_frames(data):
    value = data.value
    bbox, frame_number, frame, label, plate_text  = _deserialize_image(value) # plate text
    # bbox, label, frame_number, frame,  = _deserialize_image(value) # plate
    # processing_id, motorcycle_id, frame_number, frame, bbox = _deserialize_image(value) # motor

    resized_frame = image_matrix.resizeAndPad(frame)
    [x, y, w, h] = bbox

    cv2.rectangle(resized_frame, (x, y), (w, h), (0, 255, 0), 2)
    cv2.imshow(label + ' :: ' + plate_text, resized_frame) # plate text
    # cv2.imshow(label, resized_frame) # plate
    # cv2.imshow('motorcycle', resized_frame) # motor
    cv2.waitKey(10000)