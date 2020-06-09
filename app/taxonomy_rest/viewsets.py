from rest_framework import viewsets
from rest_framework import generics
from rest_framework import permissions
from taxonomy.models import Family, Subfamily, Genus, Species
from taxonomy_rest.serializers import FamilySerializer, SubfamilySerializer, GenusSerializer, SpeciesSerializer


class FamilyViewset(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAdminUser]

    queryset = Family.objects.all()
    serializer_class = FamilySerializer

    def get_queryset(self):

        qs = Family.objects.all()
        requested_family = self.request.query_params.get('family')

        if requested_family is not None:
            requested_family = str(requested_family)
            return qs.filter(name__icontains=requested_family)
      
        return qs


class SubfamilyViewset(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAdminUser]

    queryset = Subfamily.objects.all()
    serializer_class = SubfamilySerializer

    def get_queryset(self):

        qs = Subfamily.objects.all()
        requested_subfamily = self.request.query_params.get('subfamily')

        if requested_subfamily is not None:
            requested_subfamily = str(requested_subfamily)
            
            return qs.filter(name__icontains=requested_subfamily)
        
        return qs

class GenusViewset(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAdminUser]

    queryset = Genus.objects.all()
    serializer_class = GenusSerializer

    def get_queryset(self):

        qs = Genus.objects.all()
        requested_genus = self.request.query_params.get('genus') #.lower()

        print('requested_genus', requested_genus)

        if requested_genus is not None:
            requested_genus = str(requested_genus)
            
            return qs.filter(name__icontains=requested_genus)
      
        return qs


class SpeciesViewset(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAdminUser]

    queryset = Species.objects.all()
    serializer_class = SpeciesSerializer

    def get_queryset(self):

        qs = Species.objects.all()
        requested_genus = self.request.query_params.get('genus') #.lower()

        print('requested_genus', requested_genus)

        if requested_genus is not None:
            requested_genus = str(requested_genus)
            qs_genus = Genus.objects.all()
            qs_genus = qs_genus.filter(name__iexact=requested_genus)[0]
            print(qs_genus.id)
            qs_genus_id = qs_genus.id

            return qs.filter(parent=qs_genus_id)
      
        return qs
