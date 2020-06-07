from rest_framework import serializers

from image.models import Image

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ('pk',
                    'image_name',
                    'image_date',
                    'added_date',
                    'added_by',
                    'copyright',
                    'image_type')
