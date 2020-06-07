from rest_framework import viewsets
from rest_framework import permissions
from predmodel_rest.serializers import PredModelSerializer
from predmodel.models import PredModel

class PredModelViewset(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAdminUser]
    throttle_scope = 'predictions_burst'
    throttle_scope = 'predictions_sustained'

    queryset = PredModel.objects.all()
    serializer_class = PredModelSerializer



