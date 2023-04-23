from PIL import Image
import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt
from keras.applications.inception_v3 import preprocess_input

def url_to_array(file_path): 
  img = Image.open(file_path)
  new_size = (160,240)
  img = img.resize(new_size)
  img_arr = np.asarray(img,dtype="uint8")

  return img_arr

def img_to_embedding(image,model):
  try:
      image = image.reshape((1, image.shape[0], image.shape[1], image.shape[2]))
      img_preprocessed = preprocess_input(image)
      features = model.predict(img_preprocessed)
  except Exception as error: 
      print("An exception occurred on line")
      print(error)
  
  return features

def url_to_embedding(file_path,model):
  img_arr = url_to_array(file_path)
  features = img_to_embedding(img_arr,model)
  return features