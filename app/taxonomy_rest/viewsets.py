from rest_framework import viewsets
from rest_framework import permissions
from taxonomy.models import Family, Subfamily, Genus, Species
from taxonomy_rest.serializers import FamilySerializer, SubfamilySerializer, GenusSerializer, SpeciesSerializer


class FamilyViewset(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAdminUser]

    queryset = Family.objects.all()
    serializer_class = FamilySerializer

class SubfamilyViewset(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAdminUser]

    queryset = Subfamily.objects.all()
    serializer_class = SubfamilySerializer

class GenusViewset(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAdminUser]

    queryset = Genus.objects.all()
    serializer_class = GenusSerializer

class SpeciesViewset(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAdminUser]

    queryset = Species.objects.all()
    serializer_class = SpeciesSerializer