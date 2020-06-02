from rest_framework.response import Response
from rest_framework import status
from backend.settings import DEBUG

from predmodel.models import PredModel 

import numpy as np
from PIL import Image
import requests
import json
import ast
dictionary = ast.literal_eval("{'a': 1, 'b': 2}")


MODEL_NAME = 'resnet_test'
MODEL_VERSION = 'v1'
TENSORFLOW_SERVING_URL = 'http://tf:8501/{version}/models/{model_name}:predict'.format(version=MODEL_VERSION, model_name=MODEL_NAME)

FAKE_MODEL_RESPONSE = False

MEAN_RGB = [142.09, 133.11, 119.00]
MEAN_RGB = np.array(MEAN_RGB) / 255

STDDEV_RGB = [92.01, 90.91, 88.99]
STDDEV_RGB = np.array(STDDEV_RGB) / 255


def get_model_rgb_mean_and_stddev(model_name=None):
    
    """queries database for values for rgb_mean and rgb_stddev (which were used for a specific model's training)
    if model_name is none, gets the values for the latest model"""
    
    if model_name == None:
        # use the latest pushed model
        pred_model = PredModel.objects.last()

    else:
        pred_model = PredModel.objects.filter(name=model_name)[0]

    model_name = pred_model.name
    mean_rgb = pred_model.rgb_mean_values
    mean_rgb = ast.literal_eval(mean_rgb)
    stddev_rgb = pred_model.stddev_rgb_values
    stddev_rgb = ast.literal_eval(stddev_rgb)

    return mean_rgb, stddev_rgb


def normalize_image(img_array, mean_rgb, stddev_rgb):

    img_array_pre = img_array / 255
    img_array_norm = img_array_pre - mean_rgb
    img_array_norm = img_array_norm / stddev_rgb
    
    return img_array_norm

def preprocess_img_for_prediction(image_localpath, model_name=None):

    mean_rgb, stddev_rgb = get_rgb_mean_and_stddev(model_name=model_name)

    img = Image.open(image_localpath)
    img = np.array(img, mean_rgb, stddev_rgb)
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
        if DEBUG:
            print('logging: posting image to model')
        model_api_response = requests.post(TENSORFLOW_SERVING_URL, data=data, headers=headers)
   
    return model_api_response 