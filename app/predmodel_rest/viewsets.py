from rest_framework import viewsets
from rest_framework import permissions
from predmodel_rest.serializers import PredModelSerializer
from predmodel.models import PredModel

class PredModelViewset(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAdminUser]

    queryset = PredModel.objects.all()
    serializer_class = PredModelSerializer



