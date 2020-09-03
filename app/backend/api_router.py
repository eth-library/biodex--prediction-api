from rest_framework import routers
from django.urls import path, include

#viewsets
from taxonomy_rest.viewsets import FamilyViewset, SubfamilyViewset, GenusViewset, SpeciesViewset
from predmodel_rest.viewsets import PredModelViewset
from image.viewsets import ImageViewset
from imageClassification_rest.viewsets import ImageClassificationViewset
#functional views
from uploadforpredict_rest.views import predict_image_view
from imageClassification_rest.viewsets import LabelledImagesList
from taxonomy_rest.viewsets import query_species_name

router = routers.DefaultRouter()
# router viewsets
#prediction model endpoints
router.register(r'models', PredModelViewset)

## taxonomy endpoints
router.register(r'taxonomy/family', FamilyViewset)
router.register(r'taxonomy/subfamily', SubfamilyViewset)
router.register(r'taxonomy/genus', GenusViewset)
router.register(r'taxonomy/species', SpeciesViewset)
#media endpoints
router.register(r'images/classifications', ImageClassificationViewset)
router.register(r'images', ImageViewset)

paths = [
    path("auth/", include("djoser.urls")),
    path("predict", predict_image_view, name='api-predict'),
    path('images/training', LabelledImagesList.as_view()),
    path('query_species', query_species_name),
    ]

router_urls = paths  + router.urls