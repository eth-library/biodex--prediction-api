from rest_framework import serializers

from imageClassification.models import ImageClassification

class ImageClassificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageClassification
        fields = '__all__'

class TrainingImagesSerializer(serializers.Serializer):
    family_key = serializers.IntegerField(source='family_key__pk', allow_null=True)
    subfamily_key = serializers.IntegerField(source='subfamily_key__pk', allow_null=True)
    genus_key = serializers.IntegerField(source='genus_key__pk', allow_null=True)
    species_key = serializers.IntegerField(source='species_key__pk', allow_null=True)
    image_pk = serializers.IntegerField(source='image_key__pk')
    image_path = serializers.CharField(source='image_key__image', max_length=250)
