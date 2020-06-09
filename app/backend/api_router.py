from rest_framework import routers

from taxonomy_rest.viewsets import FamilyViewset, SubfamilyViewset, GenusViewset, SpeciesViewset
from predmodel_rest.viewsets import PredModelViewset
from image_rest.viewsets import ImageViewset

router = routers.DefaultRouter()
# router viewsets
## taxonomy endpoints
router.register(r'^taxonomy/family', FamilyViewset)
router.register(r'taxonomy/subfamily', SubfamilyViewset)
router.register(r'taxonomy/genus', GenusViewset)
router.register(r'^taxonomy/species',SpeciesViewset)
#media endpoints
router.register(r'images', ImageViewset)
#prediction model endpoints
router.register(r'models', PredModelViewset)

