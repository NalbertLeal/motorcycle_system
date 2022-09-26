import cv2
import numpy as np

from .image_matrix import resizeAndPad, resize_image, normalize, add_batch_dimension

YOLOv5_IMAGE_HEIGHT = 640
YOLOv5_IMAGE_WIDTH = 640

def preprocess_image_to_onnx(frame: np.ndarray, preserve_aspect_ratio: bool=False) -> np.ndarray:
    '''
        Prepare image to an onnx model process.
    '''
    if preserve_aspect_ratio:
        img = resizeAndPad(frame)
    else:
        img = resize_image(frame, YOLOv5_IMAGE_HEIGHT, YOLOv5_IMAGE_WIDTH)
    img = to_onnx_format(img, YOLOv5_IMAGE_HEIGHT, YOLOv5_IMAGE_WIDTH)
    img = normalize(img)
    img = add_batch_dimension(img)
    return img

def to_onnx_format(img: np.ndarray, height: int=640, width: int=640) -> np.ndarray:
	return np.ascontiguousarray(img).astype(np.float32).transpose(2, 0, 1)