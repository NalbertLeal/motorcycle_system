import time
from typing import Tuple
import numpy as np

import cv2

# Letter - old
class_old_lett_cfg = "./nn_weights/recognition/9_gabo_oldLet.cfg"
class_old_lett_wei = "./nn_weights/recognition/9_gabo_oldLet_80000.weights"

# Number - old
class_old_numb_cfg = "./nn_weights/recognition/3_gabo_oldNum.cfg"
class_old_numb_wei = "./nn_weights/recognition/3_gabo_oldNum.weights" #100000

# Letter - new
class_new_lett_cfg = "./nn_weights/recognition/3_gabo_newLet.cfg"
class_new_lett_wei = "./nn_weights/recognition/3_gabo_newLet_40000.weights"

# Number - new
class_new_numb_cfg = "./nn_weights/recognition/2_gabo_newNum.cfg"
class_new_numb_wei = "./nn_weights/recognition/2_gabo_newNum_60000.weights"  

class CharactersRecognition():
  def __init__(self):
    self.class_old_lett = cv2.dnn.readNetFromDarknet(class_old_lett_cfg, class_old_lett_wei)
    self.class_old_numb = cv2.dnn.readNetFromDarknet(class_old_numb_cfg, class_old_numb_wei)
    self.class_new_lett = cv2.dnn.readNetFromDarknet(class_new_lett_cfg, class_new_lett_wei)
    self.class_new_numb = cv2.dnn.readNetFromDarknet(class_new_numb_cfg, class_new_numb_wei)

  def getOutputsNames(self, net):
    layersNames = net.getLayerNames()
    return [layersNames[i - 1] for i in net.getUnconnectedOutLayers()]

  
  def postProcessClassifier(self, outs, classes, qtd = 3):
    predictions = []
    for out in outs[0][0]:
      predictions.append(out[0][0])

    predicted_letter = [classes[l] for l in np.argsort(predictions)[::-1][:qtd]]
    confidence_result = [predictions[p] for p in np.argsort(predictions)[::-1][:qtd]]

    return predicted_letter, confidence_result

  
  def get_plate_text(self, text, confidence):
    # Ensure that there is text and confidence
    if text == [] or confidence == []:
        return '', 0

    # Initiate variables
    text_vector = []
    confidence_vector = []
    
    # Get the best one
    plate_text = ''
    plate_confidence = 0
    
    for t, c in zip(text, confidence):
      plate_text = plate_text + t[0]
      plate_confidence = plate_confidence + c[0]

    text_vector.append(plate_text)
    confidence_vector.append(round(plate_confidence/len(confidence),4))

    # Get other possibilities
    min_confidence = min(confidence, key=lambda x:x[0])            
    if(min_confidence[0] < 0.90):                                   # It means that there is one char that has a confidence level lower than 90%
      for i in range(len(confidence)):                            # It should be 7 times
        plate_text = ""
        plate_confidence = 0
        pos = 0

        for t, c in zip(text, confidence):
          if i == pos:
            if c[1] > 0.08:                                 # To be considered, the char prediction must be higher than 0.09
              plate_text = plate_text + t[1]
              plate_confidence = plate_confidence + c[1]
            else:
              plate_confidence = 0
              break
          else:
            plate_text = plate_text + t[0]
            plate_confidence = plate_confidence + c[0]
          pos+=1

        plate_confidence = plate_confidence/len(confidence)

        if(plate_confidence > 0.70):                            # It will only be considered results greater than 70%
          text_vector.append(plate_text)
          confidence_vector.append(round(plate_confidence,4))

    return text_vector, confidence_vector

  def letter_recognition(self, letter_image, letter_class, inpWidth = 20, inpHeight = 20, readImg = False):
    letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

    predicted_letter = []
    confidence_result = []

    # resizing and morphological operation
    if(readImg):        
      try:
        letter_image = cv2.imread(letter_image)
      except:
        raise EOFError("Não foi possível ler a imagem") 

    letter_image = cv2.cvtColor(letter_image,cv2.COLOR_RGB2GRAY)       # por hora, a rede nao funciona com essa configuracao!
    letter_image = cv2.resize(letter_image,(inpWidth,inpHeight),interpolation=cv2.INTER_AREA) # depois, nao vai precisar disso 
    #letter_image = self.morphological_letter(letter_image)   # morphological operation

    # apply inversion if plate is red
    # if letter_class == 'vermelha':
    #   letter_image = np.invert(letter_image)

    # preparing image for insert at NN
    letter_image = cv2.cvtColor(letter_image, cv2.COLOR_GRAY2RGB)   # gambiarra pois a rede só aceita 3 canais
    blob = cv2.dnn.blobFromImage(letter_image, 1/255, (inpHeight, inpWidth), [0,0,0], 1, crop=False)

    # prediction based on plate type
    if letter_class == 'mercosul':
      self.class_new_lett.setInput(blob)
      predictions = self.class_new_lett.forward(self.getOutputsNames(self.class_new_lett))
    else:
      self.class_old_lett.setInput(blob)
      predictions = self.class_old_lett.forward(self.getOutputsNames(self.class_old_lett))

    predicted_letter, confidence_result = self.postProcessClassifier(predictions, letters)
    
    return predicted_letter, np.around(confidence_result,3)


  # Recognizes a number given an image
  def number_recognition(self, number_image, number_class, inpWidth = 20, inpHeight = 20, readImg = False):
    numbers = '0123456789'

    predicted_number = []
    confidence_result = []

    # resizing and morphological operation
    if(readImg):        
      try:
        number_image = cv2.imread(number_image)
      except:
        raise EOFError("Não foi possível ler a imagem") 

    number_image = cv2.cvtColor(number_image,cv2.COLOR_BGR2GRAY)
    number_image = cv2.resize(number_image,(inpWidth,inpHeight),interpolation=cv2.INTER_AREA)

    # apply inversion if plate is red
    # if number_class == 'vermelha':
    #   number_image = np.invert(number_image)

    # preparing image for insert at NN
    number_image = cv2.cvtColor(number_image, cv2.COLOR_GRAY2RGB)   # gambiarra pois a rede só aceita 3 canais
    blob = cv2.dnn.blobFromImage(number_image, 1/255, (inpHeight, inpWidth), [0,0,0], 1, crop=False)

    # prediction based on plate type
    if number_class == 'mercosul':
      self.class_new_numb.setInput(blob)
      predictions = self.class_new_numb.forward(self.getOutputsNames(self.class_new_numb))
    else:
      self.class_old_numb.setInput(blob)
      predictions = self.class_old_numb.forward(self.getOutputsNames(self.class_old_numb))
    
    predicted_number, confidence_result = self.postProcessClassifier(predictions, numbers)
    
    return predicted_number, np.around(confidence_result,3)

  def recognition(self, plate_img, plate_class, char_positions, is_fst_half=True):
    plate_text = []
    plate_confidence = []

    # for each detected plate, 
    # for c_pos in char_positions:
    text = []                                   # Text of each plate individually
    confidence = []                             # Confidente level of each plate individually

    if len(char_positions) == 3 or len(char_positions) == 4:                         # number of detected chars is seven    
      pos = 0
      for rec in char_positions:                       # going over each character 
        rec = [max(0,i) for i in rec]       # ensuring that there is no negative value.
        char_image = plate_img[rec[1]:(rec[1]+rec[3]),rec[0]:(rec[0]+rec[2])]
        if plate_class == 'mercosul': # classe 'nova' no sistema lpr
          if is_fst_half or pos in [1]:
            predicted_letter, confidence_result = self.letter_recognition(char_image, plate_class)
            text.append(predicted_letter)
            confidence.append(confidence_result)
          else:
            predicted_number, confidence_result = self.number_recognition(char_image, plate_class)
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
            predicted_letter, confidence_result = self.letter_recognition(char_image, plate_class)
            text.append(predicted_letter)
            confidence.append(confidence_result)
          else:
            predicted_number, confidence_result = self.number_recognition(char_image, plate_class)
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
        pos+=1

    else:                                           # number of chars is not seven
      for rec in char_positions:                           # going over each character
        rec = [max(0,i) for i in rec]           # ensuring that there is no negative value.
        char_image = plate_img[rec[1]:(rec[1]+rec[3]),rec[0]:(rec[0]+rec[2])]
        
        # Predict values
        predicted_letter, confidence_letter = self.letter_recognition(char_image, plate_class, 2)
        predicted_number, confidence_number = self.number_recognition(char_image, plate_class, 2)

        # Ordering values
        index = np.argsort(confidence_letter.tolist()+confidence_number.tolist())[::-1][:]
        confidence_char = [(confidence_letter.tolist()+confidence_number.tolist())[i] for i in index]
        predicted_char = [(predicted_letter+predicted_number)[i] for i in index]
        
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