from rest_framework import serializers
from taxonomy.models import Family, Subfamily, Genus, Species

class FamilySerializer(serializers.ModelSerializer):
    class Meta:
        model = Family
        fields = ('id','name','created_date')


class SubfamilySerializer(serializers.ModelSerializer):
    class Meta:
        model = Subfamily
        fields = ('id','name','parent','created_date')


class GenusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genus
        fields = ('id','name','parent','created_date')


class SpeciesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Species
        fields = ('id','name','parent','created_date')


