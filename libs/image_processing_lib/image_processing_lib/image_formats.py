import cv2
import io
import numpy as np
from typing import Tuple

YOLOv5_IMAGE_HEIGHT = 640
YOLOv5_IMAGE_WIDTH = 640

def _img_compress(format: str, frame: np.ndarray) -> bytes:
    format_extension = f'.{format}'
    is_success, buffer = cv2.imencode(format_extension, frame)
    if not is_success:
        raise BaseException('Image compression with a problem')
    io_buf = io.BytesIO(buffer)
    io_buf.seek(0)
    content = io_buf.read()
    io_buf.close()
    return content

def matrix_to_png(img: np.ndarray) -> bytes:
    return _img_compress('png', img)

def matrix_to_jpg(img: np.ndarray) -> bytes:
    return _img_compress('jpg', img)

def _image_to_matrix(img: bytes) -> np.ndarray:
    buffer = io.BytesIO(img)
    img = cv2.imdecode(np.frombuffer(buffer.getbuffer(), np.uint8), -1)
    buffer.close()
    return img

def png_to_matrix(img: bytes) -> np.ndarray:
    return _image_to_matrix(img)

def jpg_to_matrix(img: bytes) -> np.ndarray:
    return _image_to_matrix(img)