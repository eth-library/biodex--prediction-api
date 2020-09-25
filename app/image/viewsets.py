from rest_framework import viewsets
from rest_framework import permissions

from image.models import Image
from image.serializers import ImageSerializer
from backend import custom_permissions

class ImageViewset(viewsets.ModelViewSet):

    """
    list:
    Returns a list of all images in the BioDex database that are used for displaying examples of species and for training models. (excludes uploaded images).
    
    retrieve:
    Return a specific image.

    create:
    add a new image to the BioDex database. These images should be prescreened and have the appropriate permission for displaying to other users.
    Images uploaded for classification are not saved with this endpoint.

    update:
    change some of the information  fields for a specific image
    """    
    
    permission_classes = [custom_permissions.IsAdminUserOrReadOnly]

    queryset = Image.objects.all()
    serializer_class = ImageSerializer