from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from rest_framework import permissions

from imageClassification.models import ImageClassification
from imageClassification_rest.serializers import ImageClassificationSerializer

class ImageClassificationViewset(viewsets.ModelViewSet):

    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    queryset = ImageClassification.objects.all()
    serializer_class = ImageClassificationSerializer