import os
from collections import namedtuple

import numpy as np
import onnxruntime as onnx

from .onnx_posprocess import non_max_suppression_np

SUPPORTED_DEVICES = {
	'cpu': {
		'provider': 'CPUExecutionProvider',
	},
	'gpu': {
		'provider': 'CUDAExecutionProvider'
	},
	'tpu': {
		'provider': 'TensorrtExecutionProvider',
	}
}

class YOLOv5Onnx:
  def __init__(self, device, session):
    self.device = device
    self.session = session

def new_YOLOv5Onnx(weights: str, device: str) -> YOLOv5Onnx:
	if not _is_acceptable_device(device):
		raise BaseException('Device not acceptable')
	if not _does_weights_file_exists(weights):
		raise BaseException('Weights file not found')
	session = _create_session(weights, device)
	return YOLOv5Onnx(device=device, session=session)

def _is_acceptable_device(device: str) -> bool:
	return device in SUPPORTED_DEVICES.keys()

def _does_weights_file_exists(weights: str) -> bool:
	return os.path.exists(weights)

def _create_session(weights: str, device: str) -> onnx.InferenceSession:
	try:
		provider = SUPPORTED_DEVICES[device]['provider']
		model = onnx.InferenceSession(weights, providers=[provider])
		return model
	except:
		providers = onnx.get_available_providers()
		raise BaseException('Problem while creating the model.\nThe available providers are ' + providers)

def run_model(model: YOLOv5Onnx, img: np.ndarray, conf_thres=0.25, iou_thres=0.45):
    '''
        Run an image on an onnx model
    '''
    output_name = model.session.get_outputs()[0].name
    input_name = model.session.get_inputs()[0].name
    output = model.session.run([output_name], {input_name: img})[0]
    return non_max_suppression_np(output, conf_thres=conf_thres, iou_thres=iou_thres)[0]