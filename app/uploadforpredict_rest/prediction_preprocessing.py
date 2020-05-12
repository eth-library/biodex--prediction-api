from rest_framework.response import Response
from rest_framework import status

import numpy as np
from PIL import Image
import requests
import json


MODEL_NAME = 'resnet_test'
MODEL_VERSION = 'v1'
TENSORFLOW_SERVING_URL = 'http://localhost:8501/{version}/models/{model_name}:predict'.format(version=MODEL_VERSION, model_name=MODEL_NAME)

FAKE_MODEL_RESPONSE = True

STDDEV_RGB = [92.01, 90.91, 88.99]
STDDEV_RGB = np.array(STDDEV_RGB) / 255

MEAN_RGB = [142.09, 133.11, 119.00]
MEAN_RGB = np.array(MEAN_RGB) / 255


def normalize_image(img_array):
        
    img_array_pre = img_array / 255
    img_array_norm = img_array_pre - MEAN_RGB
    img_array_norm = img_array_norm / STDDEV_RGB
    
    return img_array_norm

def preprocess_img_for_prediction(image_localpath):

    img = Image.open(image_localpath)
    img = np.array(img)
    img = normalize_image(img)    
    img = img.tolist()

    return img


def get_model_prediction(image_localpath):
    """
    loads a locally saved image and posts to the model server to get prediction results
    image_localpath: 
    """
    if FAKE_MODEL_RESPONSE:        
        model_prediction = np.zeros(60) #fake the model response if the model api is not running
        model_prediction[0] = 15
        resp_content = json.dumps({'predictions':[model_prediction,]})
        model_api_response = Response(resp_content, status.HTTP_206_PARTIAL_CONTENT)
    else:
        #load & preprocess local image
        preprocessed_img = preprocess_img_for_prediction(image_localpath)

        #format the request
        data = json.dumps({ "instances": [preprocessed_img, ]})
        headers = {"content-type": "application/json"}
        model_api_response = requests.post(TENSORFLOW_SERVING_URL, data=data, headers=headers)
   
    return model_api_response 