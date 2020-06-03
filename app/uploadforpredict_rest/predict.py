
import requests
import json
import numpy as np

from uploadforpredict_rest.prediction_preprocessing import preprocess_img

MODEL_NAME = 'resnet_test'
MODEL_VERSION = 'v1'
TENSORFLOW_SERVING_BASE_URL = 'http://tf:8501/{version}/models/{model_name}:predict'

FAKE_MODEL_RESPONSE = False


def get_model_record(model_name):
    
    if model_name == None:
        # use the latest pushed model
        model_record = PredModel.objects.last()

    else:
        model_record = PredModel.objects.filter(name=model_name)[0]

    return model_record


def format_model_request(model_record, preprocessed_img):

    model_url = TENSORFLOW_SERVING_BASE_URL.format(
                        version=MODEL_VERSION, 
                        model_name=model_record.name)
    request_data = json.dumps({ "instances": [preprocessed_img, ]})
    headers = {"content-type": "application/json"}

    return model_url, request_data, headers
    

def make_fake_model_api_response():
    model_prediction = np.zeros(60) #fake the model response if the model api is not running
    model_prediction[0] = 15
    resp_content = json.dumps({'predictions':[model_prediction,]})
    
    return Response(resp_content, status.HTTP_206_PARTIAL_CONTENT)


def get_model_prediction(image_localpath, model_name):
    """
    loads a locally saved image and posts to the model server to get prediction results
    image_localpath: 
    """

    if FAKE_MODEL_RESPONSE:
        return make_fake_model_api_response()
    
    else:
        #load & preprocess local image
        model_record = get_model_record(model_name)
        preprocessed_img = preprocess_img(image_localpath, model_record)
        request_params = format_model_request(model_record, preprocessed_img)
                                                
        model_url, request_data, headers = request_params

        if DEBUG:
            print('logging: posting image to model')
            
        model_api_response = requests.post(TENSORFLOW_SERVING_URL, 
                                            data=data, 
                                            headers=headers)
   
    return model_api_response 