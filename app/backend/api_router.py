from rest_framework import routers

from taxonomy_rest.viewsets import FamilyViewset, SubfamilyViewset, GenusViewset, SpeciesViewset
from predmodel_rest.viewsets import PredModelViewset
from images_labelled_rest.viewsets import ImageLabelledViewset

router = routers.DefaultRouter()
# router viewsets
## taxonomy endpoints
router.register(r'taxonomy/family', FamilyViewset)
router.register(r'taxonomy/subfamily', SubfamilyViewset)
router.register(r'taxonomy/genus', GenusViewset)
router.register(r'taxonomy/species', SpeciesViewset)
#prediction model endpoints
router.register(r'models', PredModelViewset)
router.register(r'images/labelled', ImageLabelledViewset)

