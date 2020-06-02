
from django.test import TestCase

# Create your tests here.

import requests
import json
import pprint
import os

url = 'https://europe-west1-ethec-auto-insect-recognition.cloudfunctions.net/lepidoptera_clfr_objdet'
url = 'http://127.0.0.1:8000/upload/'


fldr_path = './app/backend/assets/example_images/2017_03_10R/'
fname = 'ETHZ_ENT01_2017_03_10_001404.JPG'
img_path = fldr_path + fname
files = {'image': (fname, open(img_path, 'rb')) }

r = requests.post(url, files=files)
print('status code: ', r.status_code)
if r.status_code == 201:
    r_json = r.json()
    pprint.pprint(r.json())
