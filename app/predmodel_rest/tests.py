from django.test import TestCase

# Create your tests here.
import requests
import json

class ModelEndpoint(TestCase):
    
    def setUp(self):
        self.description="check that a post request to models api returns 201"
        self.url = "http://localhost:8000/api/models/"
        self.auth_token = "6a3b38c2e0555cb5a3144583fec6bf4b520ead15"
        self.headers = {'Authorization': 'Token {}'.format(self.auth_token)}
        self.data =  {
            "name": -6,
            "description": "testing model endpoint2",
            "species_included": "{1000, 1001, 1002, 1003, 1004}",
            "species_key_map": "{1000:0, 1001:1, 1002:2, 1003:3, 1004:4}",
            "encoded_hierarchy": "{0:[0,1,2,3,4], 1:[0,0,1,2,2], 2:[0,0,0,1,1], 3:[0,0,0,0,1]}"
            "rgb_mean_values":"[0, 0, 0]",
            "stddev_rgb_values":"[1, 1, 1]",
            }
        self.id = None

    def test_post_and_delete(self):
        
        resp = requests.post(self.url, headers=self.headers, data=self.data)
        resp_json = json.loads(resp.content)
        print('test post returned: ', resp.status_code)
        self.assertEqual(resp.status_code, 201)
        self.id = resp_json['id']
        # delete this record
        del_url = self.url + str(self.id) + "/"
        resp = requests.delete(del_url, headers=self.headers)
        print('test_delete returned: ', resp.status_code)
        assertion_test = resp.status_code in [200, 201, 202, 204]
        self.assertEqual(True, assertion_test)
