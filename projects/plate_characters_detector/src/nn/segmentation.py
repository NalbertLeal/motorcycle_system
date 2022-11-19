import time
from typing import Tuple
import numpy as np

import cv2

# SEGMENTATION_CFG = './nn_weights/segmentation/yolov4-tiny-ufpr-ufrnv178-prf-224x64_v9.cfg'
# SEGMENTATION_WEIGHTS = './nn_weights/segmentation/yolov4-tiny-ufpr-ufrnv178-prf-224x64_best_v9.weights'

class CharactersSegmentation():
    def __init__(self, seg_net) -> None:
        self.seg_net = seg_net
        # self.seg_net = cv2.dnn.readNetFromDarknet(
        #     SEGMENTATION_CFG,
        #     SEGMENTATION_WEIGHTS
        # )
        # # self.seg_net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
        # # self.seg_net.setPreferableTarget(cv2.dnn.DNN_TARGET_OPENCL_FP16)
        # self.seg_net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
        # self.seg_net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA_FP16)
        # self.seg_net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)

        self.confidence_threshold = 0.3
        self.nms_threshold = 0.1                   
        self.seg_classes = ["segmento"]
        self.pad = [0,1,1,0]

    def image_to_blob(self, img, width, height):
        return cv2.dnn.blobFromImage(
            img,
            1/255,
            (width, height),
            [0,0,0],
            1,
            crop=False
        )

    def plate_class(self, plate_type: int) -> str:
        if plate_type == 0:
            return 'mercosul'
        else:
            return 'brazil'

    def get_outputs_names(self, network):
        layersNames = network.getLayerNames()
        return [layersNames[i - 1] for i in network.getUnconnectedOutLayers()]

    def segment_plate(self, blob):
        '''
        
        '''
        self.seg_net.setInput(blob)
        return self.seg_net.forward(
            self.get_outputs_names(self.seg_net)
        )

    def get_chars_position(self, indices, boxes, confidences):
        char_position = []
        confidences_seg = []
        for i in indices: 
            box = [
                boxes[i][0]-self.pad[3],
                boxes[i][1]-self.pad[0],
                boxes[i][2]+self.pad[1],
                boxes[i][3]+self.pad[2]
            ]
            (box[0], box[1]) = (box[0], box[1])
            char_position.append(box)
            confidences_seg.append(confidences[i])
        return char_position, confidences_seg
    
    def postProcess(self, outs, img, confThreshold, nmsThreshold, name):
        classNames = []
        confidences = []
        boxes = []

        (H, W) = img.shape[:2]

        for out in outs:
            for detection in out:
                scores = detection[5:]                          # Gets the scores  
                classId = np.argmax(scores)                     # Get the class Id with the best confidence vale
                confidence = scores[classId]                    # Get the confidence of the best value!
                
                if confidence > confThreshold:
                    box = detection[0:4] * np.array([W, H, W, H])
                    (centerX, centerY, width, height) = box

                    x = int(centerX - (width / 2))
                    y = int(centerY - (height / 2))

                    classNames.append(name[classId])
                    confidences.append(float(confidence))
                    boxes.append([x, y, int(width), int(height)])     
        indices = cv2.dnn.NMSBoxes(boxes, confidences, confThreshold, nmsThreshold)   

        return indices, boxes, classNames, confidences

    def posprocessing(self, model_output, img):
        return self.postProcess(
            model_output,
            img,
            self.confidence_threshold,
            self.nms_threshold,
            self.seg_classes
        )

    def sort_char_position(self, char_position):
        if(len(char_position) != 0):
            return sorted(char_position, key=lambda x: x[0])
            # sorted_by_y_axis = sorted(char_position, key=lambda x: x[1])
            # row1 = sorted_by_y_axis[:3]
            # row2 = sorted_by_y_axis[3:]
            # row1_sorted = sorted(row1, key=lambda x: x[0])
            # row2_sorted = sorted(row2, key=lambda x: x[0])
            # return [*row1_sorted, *row2_sorted]

    def run(self, img: np.ndarray, inpWidth: int=224,\
        inpHeight: int=64) -> Tuple[Tuple[int]]:

        blob = self.image_to_blob(img, inpWidth, inpHeight)

        output = self.segment_plate(blob)
        
        indexes, boxes, _, confidences = self.posprocessing(output, img)

        char_position, confidences_seg = self.get_chars_position(
            indexes,
            boxes,
            confidences
        )

        if len(char_position) == 0:
            return char_position, confidences_seg
        sorted_char_position = self.sort_char_position(char_position) # MOTO
        if sorted_char_position is None:
            return [], confidences_seg
        # sorted_char_position = sorted(char_position, key=lambda x: x[0]) # CARRO

        return sorted_char_position, confidences_seg