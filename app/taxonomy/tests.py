from django.test import TestCase

# Create your tests here.

import requests
import json
import pprint
import os

from django.contrib.auth import get_user_model
from rest_framework.test import APIRequestFactory
from rest_framework.test import force_authenticate
from rest_framework import status
from rest_framework.test import APITestCase
from taxonomy.models import Family, Subfamily, Genus, Species
from taxonomy.viewsets import FamilyViewset, SubfamilyViewset, GenusViewset, SpeciesViewset

User = get_user_model()

class TaxonomyTests(APITestCase):

    def setUp(self):
        
        userStaff = User.objects.create_user('tester-staff',password='test-password') 
        userStaff.is_staff=True
        userStaff.save()
        user = User.objects.create_user('tester',password='test-password') 
        user.save()

        self.user_staff = User.objects.get(username='tester-staff')
        self.user = User.objects.get(username='tester')
        return

#### Family Tests ####
    def prepare_Family_post_request(self):

        factory = APIRequestFactory()
        view = FamilyViewset.as_view({'post':'create'})
        data = {'name': 'test-family'}
        request = factory.post('/pred-api/taxonomy/family/', data=data, format='json') 
        return request, view

    def test_create_Family_user(self):
        """
        Ensure that normal users cannot create Family objects
        """
        request, view = self.prepare_Family_post_request()
        force_authenticate(request, user=self.user)
        response = view(request)
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Family.objects.count(), 0)

    def test_create_Family_staff(self):
        """
        Ensure we can create a new Family object with staff user.
        """
        request, view = self.prepare_Family_post_request()
        force_authenticate(request, user=self.user_staff)
        response = view(request)
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Family.objects.count(), 1)
        self.assertEqual(Family.objects.get().name, 'test-family')

#### Subfamily Tests ####
    def prepare_Subfamily_post_request(self):

        factory = APIRequestFactory()
        view = SubfamilyViewset.as_view({'post':'create'})

        #subfamily needs to reference a related parent Family
        f = Family.objects.create(name='test-family',pk=1)
        f.save()
        data = {'name': 'test-subfamily',
                'parent':1}
        request = factory.post('/pred-api/taxonomy/subfamily/', data=data, format='json') 
        return request, view

    def test_create_Subfamily_user(self):
        """
        Ensure that normal users cannot create Family objects
        """
        request, view = self.prepare_Subfamily_post_request()
        force_authenticate(request, user=self.user)
        response = view(request)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Subfamily.objects.count(), 0)
    
    def test_create_Subfamily_staff(self):
        """
        Ensure we can create a new Family object with staff user.
        """
        request, view = self.prepare_Subfamily_post_request()
        force_authenticate(request, user=self.user_staff)
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Subfamily.objects.count(), 1)
        self.assertEqual(Subfamily.objects.get().name, 'test-subfamily')