from rest_framework import viewsets
from rest_framework import permissions

from image.models import Image
from image.serializers import ImageSerializer

class ImageViewset(viewsets.ModelViewSet):

    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    queryset = Image.objects.all()
    serializer_class = ImageSerializer