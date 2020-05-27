from rest_framework import routers

from taxonomy_rest.viewsets import FamilyViewset, SubfamilyViewset, GenusViewset, SpeciesViewset

router = routers.DefaultRouter()
# router viewsets
## taxonomy endpoints
router.register(r'taxonomy/family', FamilyViewset)
router.register(r'taxonomy/subfamily', SubfamilyViewset)
router.register(r'taxonomy/genus', GenusViewset)
router.register(r'taxonomy/species', SpeciesViewset)
