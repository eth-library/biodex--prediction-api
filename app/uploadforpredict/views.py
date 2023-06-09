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

# not in model
# Add in parameter model name into query
@api_view(['POST',])
def predict_image_view(request):
    """
    post:
    post an image for prediction. Image must be in the correct format for the prediction model. Usually 224x224 pixels.
    accepts the query parameter 'model_name' to select a specific model. Otherwise defaults to default model (e.g. 201911171137)
    
    RETURNS the prediction probabilities, species names and example images in the 'predictions' attribute of the response object.
    
    
    """
    
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
        default_model_name=201911171137
        model_name = request.query_params.get('model_name', default_model_name)

        if DEBUG:
            print('model_name: ', model_name)

        predictions_response = get_prediction(img_stream, model_name=model_name)

        if predictions_response.status_code != 200:
            return predictions_response

        response_data = {}
        response_data['uploaded_image_saved_name']  = serialized_fname
        response_data['predictions'] = predictions_response.data
        response_data['prediction_model'] = str(model_name)
        response_data['exec_time'] = str(time() - strt_time) + ' s'
        
        return Response(response_data, status=status.HTTP_201_CREATED)