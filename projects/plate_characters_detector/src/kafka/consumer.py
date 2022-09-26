from os import environ
from typing import Tuple

import numpy as np

from kafka_lib import consumer as lib_consumer
import frame_pb2 as frame_pb

def deserialize(data: bytes) -> Tuple:
    message = frame_pb.FrameMessage()
    message.ParseFromString(data)

    frame = np.frombuffer(
        message.frame.frame,
        dtype=np.float32).reshape(message.frame.shape
    )
    return message.processing_id, message.frame.frame_number, frame

def receive_image(data: bytes):
    image_png, plate_class = deserialize(data)
    # image to frame
    # resize frame to 224x64x3
    # pass frame to segmentation
    # send segmentation result to database
    # pass segmentation result to recognition
    # send recognition result to database