from rest_framework import routers
from django.urls import path, include
from rest_framework.documentation import include_docs_urls
from rest_framework.permissions import IsAuthenticated

#viewsets
from taxonomy.viewsets import FamilyViewset, SubfamilyViewset, GenusViewset, SpeciesViewset
from predmodel.viewsets import PredModelViewset
from image.viewsets import ImageViewset
from imageClassification.viewsets import ImageClassificationViewset
#functional views
from uploadforpredict.views import predict_image_view
from imageClassification.viewsets import LabelledImagesList
from taxonomy.viewsets import query_species_name

router = routers.DefaultRouter()
# router viewsets
#prediction model endpoints
router.register(r'prediction-models', PredModelViewset)

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
    path('docs/', include_docs_urls(title='BioDex - Prediction API', permission_classes=[IsAuthenticated])),
    ]

router_urls = paths  + router.urls