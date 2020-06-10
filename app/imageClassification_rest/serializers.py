from rest_framework import serializers

from imageClassification.models import ImageClassification

class ImageClassificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageClassification
        fields = '__all__'