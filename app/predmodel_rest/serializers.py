from rest_framework.serializers import ModelSerializer

from predmodel.models import PredModel

class PredModelSerializer(ModelSerializer):
    class Meta:
        model = PredModel
        fields = ('id',
                  'name',
                  'date_added',
                  'description',
                  'species_included',
                  'species_key_map',
                  'encoded_hierarchy')