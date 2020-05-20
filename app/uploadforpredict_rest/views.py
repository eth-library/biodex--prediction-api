from rest_framework import status, viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response

from time import time
import os
import json

from uploadforpredict_rest.serializers import PredictImageSerializer
from uploadforpredict.models import PredictImage
from uploadforpredict_rest.prediction_preprocessing import get_model_prediction
from uploadforpredict_rest.prediction_postprocessing import process_model_response
from backend.settings import MEDIA_ROOT, ASSETS_DIR, DEBUG

FAKE_MODEL_RESPONSE = False

@api_view(['POST','GET'])
def predict_image_view(request):
    """
    post an image for prediction
    """

    if request.method == 'POST':
        serializer = PredictImageSerializer(data=request.data)

        if serializer.is_valid():
            if DEBUG:
                print('logging: serializer.is_valid')
            strt_time = time()
            serializer.save()
            #get prediction for posted image
            response_data = serializer.data
            # request_string = str(request.data)
            serialized_fname = os.path.basename(serializer.data['image'])

            uploaded_img_path = MEDIA_ROOT + '/' +  serialized_fname

            if FAKE_MODEL_RESPONSE:
                response_data = {}
                model_api_response = get_model_prediction(uploaded_img_path)

                if model_api_response.status_code == 206:
                    predictions_data = {'fake prediction':{'predictions':str([912,1,2,2,1,2,3,4])}}
                
            else:
                model_api_response = get_model_prediction(uploaded_img_path)

                if model_api_response.status_code == 200:

                    if DEBUG:
                        print('logging: serializer.is_valid')                       
                    
                    model_api_json_resp = json.loads(model_api_response.text)
                    #possible to post a list of images to the model endpoint, but we only handle 1 image so use 0th reponse
                    model_prediction = model_api_json_resp['predictions'][0] 
                    # process model response and create predictions dictionary with example images
                    predictions_data = process_model_response(model_prediction)

                else:
                    #handle this error somehow
                    # return HTTP bad response e.g.
                    if DEBUG:
                        print('logging: error with model prediction')
                        
                    return Response('prediction model error', status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
            response_data['uploaded_image_saved_name']  = serialized_fname

            # response_data['request_string'] = request_string
            response_data['predictions'] = predictions_data
            # response_data['model'] = MODEL_NAME + '_' + MODEL_VERSION
            response_data['exec_time'] = str(time() - strt_time) + ' s'
            
            return Response(response_data, status=status.HTTP_201_CREATED)
            

    return Response("only accepts POST Requests with the field 'image'", status=status.HTTP_400_BAD_REQUEST)