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
    _img_compress('png', img)

# def matrix_to_jpg(
#     img: np.ndarray,
#     size: Tuple=(YOLOv5_IMAGE_HEIGHT, YOLOv5_IMAGE_WIDTH),
# ) -> bytes:
#     ...

def matrix_to_jpg(img: np.ndarray) -> bytes:
    _img_compress('jpg', img)

def image_to_matrix(
    img: bytes,
    extension: str='jpg',
    size: Tuple=(YOLOv5_IMAGE_HEIGHT, YOLOv5_IMAGE_WIDTH),
) -> np.ndarray:
    ...

def png_to_matrix(
    img: bytes,
    size: Tuple=(YOLOv5_IMAGE_HEIGHT, YOLOv5_IMAGE_WIDTH),
) -> np.ndarray:
    return image_to_matrix(img, 'png', size)

def jpg_to_matrix(
    img: bytes,
    size: Tuple=(YOLOv5_IMAGE_HEIGHT, YOLOv5_IMAGE_WIDTH),
) -> np.ndarray:
    return image_to_matrix(img, 'jpg', size)