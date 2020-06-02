from rest_framework import serializers

from images_labelled.models import ImageLabelled

class ImageLabelledSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageLabelled
        fields = ('pk', 'image', 'specieskey', 'added_date', 'added_by', 'copyright')
