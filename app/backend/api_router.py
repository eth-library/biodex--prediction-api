from rest_framework import routers

from taxonomy_rest.viewsets import FamilyViewset, SubfamilyViewset, GenusViewset, SpeciesViewset

router = routers.DefaultRouter()
# router viewsets
## taxonomy endpoints
router.register(r'family', FamilyViewset)
router.register(r'subfamily', SubfamilyViewset)
router.register(r'genus', GenusViewset)
router.register(r'species', SpeciesViewset)
