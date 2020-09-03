from rest_framework.serializers import ModelSerializer

from predmodel.models import PredModel

class PredModelSerializer(ModelSerializer):
    class Meta:
        model = PredModel
        fields = '__all__'