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

class ImageClassificationViewset(viewsets.ModelViewSet):

    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

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