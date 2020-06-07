import requests
import json
import numpy as np
from backend.settings import TENSORFLOW_SERVING_BASE_URL

from uploadforpredict_rest.prediction_preprocessing import preprocess_img
from uploadforpredict_rest.prediction_postprocessing import process_model_response

# MODEL_NAME = 'resnet_test'
# MODEL_VERSION = 'v1'
# TENSORFLOW_SERVING_BASE_URL = 'http://tf:8501/{version}/models/{model_name}:predict'
FAKE_MODEL_RESPONSE = False

def get_model_record(model_name):
    
    if model_name == None:
        # use the latest pushed model
        model_record = PredModel.objects.last()

    else:
        model_record = PredModel.objects.filter(name=model_name)[0]

    return model_record


def format_model_request(model_record, preprocessed_img):


    model_version = getattr(model_record, 'version', 'v1')
    model_url = TENSORFLOW_SERVING_BASE_URL.format(
                        version=model_version,
                        model_name=model_record.name)
    request_data = json.dumps({ "instances": [preprocessed_img, ]})
    headers = {"content-type": "application/json"}

    return model_url, request_data, headers


def make_fake_model_api_response():
    model_prediction = np.zeros(60) #fake the model response if the model api is not running
    model_prediction[0] = 15
    resp_content = json.dumps({'predictions':[model_prediction,]})
    
    return Response(resp_content, status.HTTP_206_PARTIAL_CONTENT)


def post_to_model(model_record, preprocessed_img):
    
    request_params = format_model_request(model_record, preprocessed_img)
    model_url, request_data, headers = request_params
        
    model_api_response = requests.post(model_url, 
                                        data=data, 
                                        headers=headers)

    return model_api_response


def get_predictions(image_localpath, model_name):
    """
    loads a locally saved image and posts to the model server to get prediction results
    image_localpath: 
    """

    model_record = get_model_record(model_name)
    preprocessed_img = preprocess_img(image_localpath, model_record)
    model_response = post_to_model(model_record, preprocessed_img)
    predictions = process_model_response(model_response)

    return predictions