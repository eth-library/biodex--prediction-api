from django.test import TestCase

# Create your tests here.

import requests
import json
import pprint
import os

import time

user_name = 'admin'
password = 'lepi-pass'

def get_token(user_name, password):

    login_url = "http://127.0.0.1:8000/api/auth/token/login/"

    payload = {'username': user_name,
                'password': password}

    resp = requests.post(login_url, json=payload)

    print(resp.status_code)
    print(resp.text)

    if resp.status_code == 200:
        resp_body = json.loads(resp.text)
        auth_token = resp_body['auth_token']
        return auth_token


auth_token = get_token(user_name, password)

def get_taxonomy(auth_token, taxonomy_level, filter_name=None):


    base_url = "http://127.0.0.1:8000/api/taxonomy/{}/".format(taxonomy_level)
    headers = {'Authorization': 'Token {}'.format(auth_token)}
    resp = requests.get(base_url, headers=headers)

    print('status_code: ', resp.status_code)

    resp_body = json.loads(resp.text)
    print(resp_body)

    return resp_body

if auth_token != None:
    for i in range(20):
        species = get_taxonomy(auth_token, 'family') 
        print('- '*50,'\n','request :', i)
        print('resp_length: ', len(species))
        time.sleep(.3)



# url = http://127.0.0.1:8000/api/taxonomy/family


# auth_token = "6a3b38c2e0555cb5a3144583fec6bf4b520ead15"
# headers = {'Authorization': 'Token {}'.format(auth_token)}

# r = requests.post(url, headers=headers, files=files)
# print('status code: ', r.status_code)
# if r.status_code == 201:
#     r_json = r.json()
#     pprint.pprint(r.json())