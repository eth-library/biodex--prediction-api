from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework import generics
from rest_framework import permissions
from rest_framework.response import Response

from taxonomy.models import Family, Subfamily, Genus, Species
from taxonomy.serializers import FamilySerializer, SubfamilySerializer, GenusSerializer, SpeciesSerializer
from backend import custom_permissions


class FamilyViewset(viewsets.ModelViewSet):
    """
    list:
    return the records for family names. Accepts the filter parameter family e.g. ?family=Lypusidae This returns any names containing the query string
    
    create:
    add a new family name to the database. Make sure to check first that the new record is 
    genuinely new and that a similar name does not already exist.

    read:
    look up a specific record by id number

    update:
    change the fields value for a specific record. For example to correct a misspelling.    

    """
    permission_classes = [custom_permissions.IsAdminUserOrReadOnly]

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
    """
    list:
    return the records for subfamily names. Accepts the filter parameter subfamily e.g. ?subfamily=Agliinae This returns any names containing the query string
    
    create:
    add a new subfamily name to the database. Make sure to check first that the new record is 
    genuinely new and that a similar name does not already exist. parent field a foreign key to the parent family

    read:
    look up a specific record by id number

    update:
    change the fields value for a specific record. For example to correct a misspelling.    

    """

    permission_classes = [custom_permissions.IsAdminUserOrReadOnly]

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
    """
    list:
    return the records for genus names. Accepts the filter parameter genus e.g. ?genus=Papilio This returns any names containing the query string
    
    create:
    add a new genus name to the database. Make sure to check first that the new record is 
    genuinely new and that a similar name does not already exist. parent field a foreign key to the parent subfamily

    read:
    look up a specific record by id number

    update:
    change the fields value for a specific record. For example to correct a misspelling.    

    """

    permission_classes = [custom_permissions.IsAdminUserOrReadOnly]

    queryset = Genus.objects.all()
    serializer_class = GenusSerializer

    def get_queryset(self):

        qs = Genus.objects.all()
        requested_genus = self.request.query_params.get('genus')

        if requested_genus is not None:
            requested_genus = str(requested_genus)
            
            return qs.filter(name__icontains=requested_genus)
      
        return qs


class SpeciesViewset(viewsets.ModelViewSet):
    """
    list:
    return the records for species names. Accepts the filter parameter genus e.g. ?genus=Papilio This returns any names containing the query string
    
    create:
    add a new genus name to the database. Make sure to check first that the new record is 
    genuinely new and that a similar name does not already exist. parent field a foreign key to the parent subfamily

    read:
    look up a specific record by id number

    update:
    change the fields value for a specific record. For example to correct a misspelling.    

    """
    permission_classes = [custom_permissions.IsAdminUserOrReadOnly]

    queryset = Species.objects.all()
    serializer_class = SpeciesSerializer

    def get_queryset(self):

        qs = Species.objects.all()
        requested_genus = self.request.query_params.get('genus')
        requested_epithet = self.request.query_params.get('epithet')

        if requested_genus is not None:
            qs = qs.filter(parent__name__icontains=requested_genus)

        # if requested_genus is not None:
        #     requested_genus = str(requested_genus)
        #     qs_genus = Genus.objects.all()
        #     qs_genus = qs_genus.filter(name__iexact=requested_genus)[0]
        #     qs_genus_id = qs_genus.id
        #     qs = qs.filter(parent=qs_genus_id)
      
    
        if requested_epithet is not None:
            qs = qs.filter(name__icontains=requested_epithet)

        return qs


class QuerySpeciesByName(APIView):
    """
    convenient way to view the string names in the database
    """
    # authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [custom_permissions.IsAdminUserOrReadOnly]
    serializer_class = SpeciesSerializer

    def get(self, request, format=None):
        """
        Look up the id number for a specific species by providing the Binomial species name.
        Accepts the parameters genus & species. e.g.
        ?genus=Archon&species=apollinus  

        This can be useful for aligning data sources
        """

        genus = request.GET.get('genus', 'Archon')
        epithet = request.GET.get('epithet', '')

        print(genus, epithet)

        qs = Species.objects.filter(parent__name=genus)
        if epithet:
            qs = qs.filter(name=epithet)
        names = [q for q in qs]

        ser = SpeciesSerializer(names, many=True)
        return Response(ser.data)