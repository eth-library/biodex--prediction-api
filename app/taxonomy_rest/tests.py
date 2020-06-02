from django.test import TestCase

# Create your tests here.

import requests
import json
import pprint
import os

url = ' http://127.0.0.1:8000/api/family/'

print('\n get\n ')
r = requests.get(url)
print('status code: ', r.status_code)
if str(r.status_code)[0] == '2':
    r_json = r.json()
    pprint.pprint(r.json())



print('\n post \n')
post_data = {'name':'Hesperidae'}
r = requests.post(url, data=post_data)
print('status code: ', r.status_code)
if str(r.status_code)[0] == '2':
    r_json = r.json()
    pprint.pprint(r.json())


