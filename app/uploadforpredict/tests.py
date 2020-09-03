from rest_framework.test import APIRequestFactory
from rest_framework.test import force_authenticate
from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from django.test import TestCase

from image.models import Image
from .prediction_postprocessing import query_example_images

class TestPredictionEndpoint(APITestCase):

    def test_anonymous_is_forbidden(self):

        response = self.client.post(reverse('api-predict'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

class TestPredictionPostProcessing(TestCase):

    def setUp(self):

        Image.objects.create()

    def test_example_images(self):
        
        query_example_images()
        
