from rest_framework import viewsets, permissions
from rest_framework.decorators import api_view

from predmodel.serializers import PredModelSerializer
from predmodel.models import PredModel

class PredModelViewset(viewsets.ModelViewSet):
    """
    list:
    list the prediction models with their metadata (e.g. hierarchy used). Note that not all of these models
    may not still be available for inference.

    create:
    add a new model record. values saved here are then used for post processing the raw model response. 

    update:
    change the values for a specific model

    read:
    return the values for a specific model

    """
    permission_classes = [permissions.IsAdminUser]
    throttle_scope = 'predictions_burst'
    throttle_scope = 'predictions_sustained'

    queryset = PredModel.objects.all()
    serializer_class = PredModelSerializer


# @api_view(['GET'])
# def latest_model_class_details(request):
#     """
#     get:
    

#     """

#     mod_key_map = PredModel.objects.all().last().species_key_map
#     db_species = list(mod_key_map.values())
