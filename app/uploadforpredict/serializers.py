from rest_framework import serializers
from uploadforpredict.models import PredictImage

class PredictImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PredictImage
        fields = ['pk', 'image']
