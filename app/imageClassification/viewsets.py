from django.shortcuts import render
from django.http import JsonResponse
from django.db.models import F

from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.pagination import LimitOffsetPagination

from imageClassification.models import ImageClassification
from imageClassification.serializers import ImageClassificationSerializer, TrainingImagesSerializer
from image.models import Image
from backend import custom_permissions

class ImageClassificationViewset(viewsets.ModelViewSet):
    """
    list: 
    return a list of classifications. These are species classifications that that have been assigned to
    images in the database by experts and admins. An image can have multiple classifications (for example if different users
    have classified the same image)
    
    create:
    add a new classification to an image. family_key, subfamily_key, 
    genus_key and species_key are foreign keys to the relevant tables in the taxonomy tables.
    
    read:
    return details for a specific classification

    update:
    change details for a specific classification

    partial_update:
    change some of the fields for a specific classification
    
    """

    permission_classes = [custom_permissions.IsAdminUserOrReadOnly]

    queryset = ImageClassification.objects.all()
    serializer_class = ImageClassificationSerializer

    def get_queryset(self):

        qs = ImageClassification.objects.all()
        spec_key = self.request.query_params.get('species_key')

        if spec_key is not None:
            spec_key = str(spec_key)
            return qs.filter(species_key=spec_key)

            return qs

        return qs

class LargeResultsSetPagination(LimitOffsetPagination):
    default_limit = 1000
    max_limit = 10000

class LabelledImagesList(ListAPIView):
    """
    get:
    Returns the image records joined with their classifications in a single table.
    Used for returning data in a convenient format for model training.
    """


    permission_classes = [custom_permissions.IsAdminUserOrReadOnly]
    queryset = ImageClassification.objects.all().values(
                        'family_key__pk',
                        'subfamily_key__pk',
                        'genus_key__pk',
                        'species_key__pk',
                        'image_key__pk',
                        'image_key__image'
    )
    pagination_class = LargeResultsSetPagination
    serializer_class = TrainingImagesSerializer