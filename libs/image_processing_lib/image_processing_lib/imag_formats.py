import cv2
import numpy as np
from typing import Tuple

YOLOv5_IMAGE_HEIGHT = 640
YOLOv5_IMAGE_WIDTH = 640

def matrix_to_png(
    img: np.ndarray,
    size: Tuple=(YOLOv5_IMAGE_HEIGHT, YOLOv5_IMAGE_WIDTH),
) -> bytes:
    ...

def matrix_to_jpg(
    img: np.ndarray,
    size: Tuple=(YOLOv5_IMAGE_HEIGHT, YOLOv5_IMAGE_WIDTH),
) -> bytes:
    ...

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