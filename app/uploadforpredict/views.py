from rest_framework import status, viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response

from time import time
import os
import json
from PIL import Image

from uploadforpredict.serializers import PredictImageSerializer
from uploadforpredict.models import PredictImage
from uploadforpredict.predict import get_prediction

from backend.settings import MEDIA_ROOT, DEBUG

FAKE_MODEL_RESPONSE = False

@api_view(['POST','GET'])
def predict_image_view(request):
    """
    post an image for prediction
    """
    
    if request.method != 'POST':
        return Response("only accepts POST Requests with the field 'image'", status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'POST':
        serializer = PredictImageSerializer(data=request.data)

        if not serializer.is_valid():
            return Response("improperly formatted request", status=status.HTTP_400_BAD_REQUEST)

        else:
            if DEBUG:
                print('logging: serializer.is_valid')

            strt_time = time()
            serializer.save()
            #get prediction for posted image

            if DEBUG:
                request_string = str(request.data)
                print(request_string)

            img_stream = request.data['image'].open()
            serialized_fname = os.path.basename(serializer.data['image'])
            #preprocess, send to model & process model results
            model_name=201911171137
            predictions_response = get_prediction(img_stream, model_name=model_name)

            if predictions_response.status_code != 200:
                return predictions_response

            response_data = {}
            response_data['uploaded_image_saved_name']  = serialized_fname

            response_data['predictions'] = predictions_response.data
            response_data['prediction_model'] = str(model_name)
            response_data['exec_time'] = str(time() - strt_time) + ' s'
            
            return Response(response_data, status=status.HTTP_201_CREATED)