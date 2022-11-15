import time
from typing import Tuple
import numpy as np

import cv2

# Letter - old
class_old_lett_cfg = "./nn_weights/recognition/9_gabo_oldLet.cfg"
class_old_lett_wei = "./nn_weights/recognition/9_gabo_oldLet_80000.weights"

# Number - old
class_old_numb_cfg = "./nn_weights/recognition/3_gabo_oldNum.cfg"
class_old_numb_wei = "./nn_weights/recognition/3_gabo_oldNum.weights"  # 100000

# Letter - new
class_new_lett_cfg = "./nn_weights/recognition/3_gabo_newLet.cfg"
class_new_lett_wei = "./nn_weights/recognition/3_gabo_newLet_40000.weights"

# Number - new
class_new_numb_cfg = "./nn_weights/recognition/2_gabo_newNum.cfg"
class_new_numb_wei = "./nn_weights/recognition/2_gabo_newNum_60000.weights"


class CharactersRecognition():
    def __init__(self):
        self.class_old_lett = cv2.dnn.readNetFromDarknet(
            class_old_lett_cfg, class_old_lett_wei)
        self.class_old_lett.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
        # self.class_old_lett.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA_FP16)
        self.class_old_lett.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)

        self.class_old_numb = cv2.dnn.readNetFromDarknet(
            class_old_numb_cfg, class_old_numb_wei)
        self.class_old_numb.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
        # self.class_old_numb.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA_FP16)
        self.class_old_numb.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)

        self.class_new_lett = cv2.dnn.readNetFromDarknet(
            class_new_lett_cfg, class_new_lett_wei)
        self.class_new_lett.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
        # self.class_new_lett.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA_FP16)
        self.class_new_lett.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)

        self.class_new_numb = cv2.dnn.readNetFromDarknet(
            class_new_numb_cfg, class_new_numb_wei)
        self.class_new_numb.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
        # self.class_new_numb.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA_FP16)
        self.class_new_numb.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)

    def run(self, plate_img, plate_class, char_positions, is_fst_half=True):
        plate_text = []
        plate_confidence = []

        # for each detected plate,
        # for c_pos in char_positions:
        text = []                                   # Text of each plate individually
        # Confidente level of each plate individually
        confidence = []

        # number of detected chars is seven
        if len(char_positions) == 3 or len(char_positions) == 4:
            pos = 0
            for rec in char_positions:                       # going over each character
                # ensuring that there is no negative value.
                rec = [max(0, i) for i in rec]
                char_image = plate_img[rec[1]:(
                    rec[1]+rec[3]), rec[0]:(rec[0]+rec[2])]
                if plate_class == 'mercosul':  # classe 'nova' no sistema lpr
                    if is_fst_half or pos in [1]:
                        predicted_letter, confidence_result = self.letter_recognition(
                            char_image, plate_class)
                        text.append(predicted_letter)
                        confidence.append(confidence_result)
                    else:
                        predicted_number, confidence_result = self.number_recognition(
                            char_image, plate_class)
                        text.append(predicted_number)
                        confidence.append(confidence_result)
                    # if pos in [0,1,2,4]:            # sequence of characters in the new class that are letters
                    #   predicted_letter, confidence_result = self.letter_recognition(char_image, plate_class)
                    #   text.append(predicted_letter)
                    #   confidence.append(confidence_result)
                    # elif pos in [3,5,6]:
                    #   predicted_number, confidence_result = self.number_recognition(char_image, plate_class)
                    #   text.append(predicted_number)
                    #   confidence.append(confidence_result)
                else:                               # old class (cinza or vermelha)
                    if is_fst_half:
                        predicted_letter, confidence_result = self.letter_recognition(
                            char_image, plate_class)
                        text.append(predicted_letter)
                        confidence.append(confidence_result)
                    else:
                        predicted_number, confidence_result = self.number_recognition(
                            char_image, plate_class)
                        text.append(predicted_number)
                        confidence.append(confidence_result)
                    # if pos in [0,1,2]:              # sequence of characters in the old class that are letters
                    #   predicted_letter, confidence_result = self.letter_recognition(char_image, plate_class)
                    #   text.append(predicted_letter)
                    #   confidence.append(confidence_result)
                    # elif pos in [3,4,5,6]:
                    #   predicted_number, confidence_result = self.number_recognition(char_image, plate_class)
                    #   text.append(predicted_number)
                    #   confidence.append(confidence_result)
                pos += 1

        else:                                           # number of chars is not seven
            for rec in char_positions:                           # going over each character
                # ensuring that there is no negative value.
                rec = [max(0, i) for i in rec]
                char_image = plate_img[rec[1]:(
                    rec[1]+rec[3]), rec[0]:(rec[0]+rec[2])]

                # Predict values
                predicted_letter, confidence_letter = self.letter_recognition(
                    char_image, plate_class, 2)
                predicted_number, confidence_number = self.number_recognition(
                    char_image, plate_class, 2)

                # Ordering values
                index = np.argsort(confidence_letter.tolist() +
                                confidence_number.tolist())[::-1][:]
                confidence_char = [
                    (confidence_letter.tolist()+confidence_number.tolist())[i] for i in index]
                predicted_char = [(predicted_letter+predicted_number)[i]
                                for i in index]

                text.append(predicted_char)
                confidence.append(confidence_char)

        # Compute score based on confidence_level and return the best plate possibilities!
        if text != []:                          # if there is not a segmentation problem
            plate_text, plate_confidence = self.get_plate_text(text, confidence)
        else:                                   # if there is a segmentation problem.
            plate_text = ['']
            plate_confidence = [0]

        plate_text.append(plate_text)
        plate_confidence.append(plate_confidence)

        return plate_text, plate_confidence
