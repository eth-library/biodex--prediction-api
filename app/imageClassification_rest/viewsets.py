from django.shortcuts import render
from django.http import JsonResponse

from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.decorators import api_view
from rest_framework.response import Response

from imageClassification.models import ImageClassification
from imageClassification_rest.serializers import ImageClassificationSerializer
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



@api_view(['GET'])
def get_example_images(request):

    print(request.data)
    # if 'species_key' in request.data.keys(): 
        # spec_key = request.data['species_key']
    spec_key = 1131
    qs = ImageClassification.objects.filter(species_key=spec_key)
    qs = qs.values('image_key')
    print(qs)

    return qs
