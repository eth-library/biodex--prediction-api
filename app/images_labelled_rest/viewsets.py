from rest_framework import viewsets
from rest_framework import permissions

from images_labelled.models import ImageLabelled
from images_labelled_rest.serializers import ImageLabelledSerializer

class ImageLabelledViewset(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAdminUser]

    queryset = ImageLabelled.objects.all()
    serializer_class = ImageLabelledSerializer