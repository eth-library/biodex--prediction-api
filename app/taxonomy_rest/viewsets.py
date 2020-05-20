from rest_framework import viewsets
from taxonomy.models import Family, Subfamily, Genus, Species
from taxonomy_rest.serializers import FamilySerializer, SubfamilySerializer, GenusSerializer, SpeciesSerializer


class FamilyViewset(viewsets.ModelViewSet):
    queryset = Family.objects.all()
    serializer_class = FamilySerializer

class SubfamilyViewset(viewsets.ModelViewSet):
    queryset = Subfamily.objects.all()
    serializer_class = SubfamilySerializer

class GenusViewset(viewsets.ModelViewSet):
    queryset = Genus.objects.all()
    serializer_class = GenusSerializer

class SpeciesViewset(viewsets.ModelViewSet):
    queryset = Species.objects.all()
    serializer_class = SpeciesSerializer