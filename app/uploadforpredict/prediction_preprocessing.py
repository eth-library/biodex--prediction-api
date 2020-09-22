from rest_framework.response import Response
from rest_framework import status
from backend.settings import DEBUG

from predmodel.models import PredModel 

import numpy as np
from PIL import Image
import requests
import json

# in a model class
def get_model_rgb_mean_and_stddev(model_record):
    
    """queries database for values for rgb_mean and rgb_stddev (which were used for a specific model's training)
    if model_name is none, gets the values for the latest model"""

    mean_rgb = model_record.rgb_mean_values
    mean_rgb = json.loads(mean_rgb)
    stddev_rgb = model_record.stddev_rgb_values
    stddev_rgb = json.loads(stddev_rgb)

    return mean_rgb, stddev_rgb

# in a model class
def normalize_image(img_array, mean_rgb, stddev_rgb):

    img_array_pre = img_array / 255
    img_array_norm = img_array_pre - mean_rgb
    img_array_norm = img_array_norm / stddev_rgb
    
    return img_array_norm

# in a model class
def preprocess_img(image_path_or_stream, model_record):

    img = Image.open(image_path_or_stream)
    img = np.array(img)

    mean_rgb, stddev_rgb = get_model_rgb_mean_and_stddev(model_record)
    img = normalize_image(img, mean_rgb, stddev_rgb)
    img = img.tolist()

    return img