# BioDex Docs


<img src="./docs_assets/BioDex_logo_name_whitebackground.jpg" height="100">

## Responsibility Matrix & Contact guidelines

This project is kindly being hosted by ETH Library.
Training new prediction models, improvements to the app or general any development work relies on contributions from our community of users.  



for general enquiries 
    
    contact@biodex@library.ethz.ch  

questions about Entomology, use in collections or discussing research colloborations

    michael.greeff@usys.ethz.ch

technical enquiries, prediction models, classification techniques etc.

    barry.sunderland@librarylab.ethz.ch

website or api services not available 

    contact@biodex@library.ethz.ch  

For general bugs or requesting new features 

    please submit an issue to the relevant github repo, or better yet, submit a pull request. see below for more info

## Responsibilites



| Task                       | ETH Library | ETH EC      | Community   |
| -----------------          | ----------- |-------------|-------------|
| Hosting                    | __✓__       |             |             |
| Deployment                 | __✓__       |             |             |
| Development                |             |             | __✓__       |
| Approving Pull Requests    |             |             | __✓__       |
| Prediction Model Training  |             |             | __✓__       |
| User Account Administration|             | __✓__       |             |
| Replying to Contact Emails |             | __✓__       |             |


<br/>
<br/>

Detail: 
<br/>

| Task                       | ETH Library | Contributors|
| -----------------          | ----------- |-------------|
| __Hosting__                |             |             |
|-- website                  |__✓__        |             |
|-- Prediction API           |__✓__        |             |
|-- Mobile API               |__✓__        |             |
| __Deployment__             |             |             |
| Prediction Model Hosting   |__✓__        |             |



## About

BioDex is a species classification tool for Taxonomists & Collection workers developed by [ETH Library Lab](https://www.librarylab.ethz.ch/).

See more at biodex.ethz.ch/about/

## Contents
1. [Project Overview](#Project-Structure-Overview)
1. [Prediction API & Website](#Prediction-API--Website)
1. [Mobile App & API](#Mobile-App--API)
1. [Image Repo (Docker Hub)](#Image-Repo)
1. [Project Maintenance & Contribution](#Maintenance-and-Contribution)
1. [Additional Info](#Additional-Info)
    * Taxonomy
    * [Podman](#Podman)
    * Copyright
    * [Django Basic Queries](#django-basic-queries)


# Project Overview




# Prediction API & Website

The _Prediction API_ is built with Django REST Framework. 
It is used to: 
- store image and taxonomic data for model training 
- act as a gateway to the prediction model (by preprocessing posted images and postprocessing model response results)
- gather response metadata (e.g. example images)
- store data from prediction requests to be used for future analysis

[Detailed README](./app/README.md)


# Mobile App & API

The mobile API is not in this codebase, for a detailed readme see that repo.

# Data

data processing is performed in a seperate repo


# Prediction Model

model training is performed in a seperate repo


# Maintenance and Contribution

This Project is kindly being hosted ETH Library. Development however is left to the open source community and anyone who like to contribute is welcome to contact us or submit a Pull Request for a new feature.  





# Additional Info

This section includes some background information and useful commands for some of the frameworks used on this project.

# Taxonomic Terminology

#### binomial naming

species are named using the binomial format where the combination of the Genus and specific epithet define a species, e.g. Homo sapiens. 

### sp.
sp. is used when the genus can be identified but the exact species cannot or does not need to be determined. e.g. Homo sp. refers to some unidentified species of the genus Homo.

# Copyright

When using images from other people/collections/entities it is very important to ensure that we have permission to distribute the images.

The BioDex project is distributed under a creative commons licence; Attribution-NonCommercial-ShareAlike 3.0 Unported (CC BY-NC-SA 3.0)
http://creativecommons.org/licenses/by-nc-sa/3.0/


# Podman

open an interactive shell on a running container

    podman exec -it <container-number> /bin/bash


## save local docker image and transfer to server

save docker image as a tar file


    docker save -o <path to generated file.tar> <image name>

Then copy your image to the host server with regular file transfer tools such as cp, scp.  
Then load the image into Docker:

    docker load -i <path to image tar file>

## using docker hub

first login to dockerhub biodex in the cmd line

    docker login

images can then be pushed or pulled from the docker hub repo
for example;

    docker push biodex/main:prediction_model__201911171137


note that there is only one private repo in the free tier so version tagging is added after double underscore instead of colon


# Rebuild and Run for Production

generate new secret keys

```python
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())
```


create an admin/superuser in the django app

```
podman exec -it WEB-CTR-NAME python manage.py createsuperuser
```


load fixture files using the convenience bash script

```
podman exec web sh load_fixtures.sh
```

connect to an interactive shell for the postgres database

```
podman exec DB-CTR-NAME psql --username=admin --dbname=biodex_dev
```



# Authentication

__Uses Djoser__

list of all available endpoints
https://djoser.readthedocs.io/en/latest/getting_started.html#available-endpoints

token endpoints
https://djoser.readthedocs.io/en/latest/token_endpoints.html

### create user
http://127.0.0.1:8000/api/auth/users/

### request token

http://127.0.0.1:8000/api/auth/token/login/


# Example Curl Requests

## Request Token
curl -X POST -d '{"username": "admin","password": "1234"}' -H 'Content-Type: application/json'  http://127.0.0.1:8000/api/auth/token/login/

## Using  Token 
curl -X POST http://127.0.0.1:8000/api/predict/ -H 'Authorization: Token a21e26bd12a16542f940d641e840e32ad16a26d0' [{"id":1,"name":"admin"]

# django basic queries

get the first 5 records from a model

    qryset = Image.objects.all()[:5]

display the field names and values for those records

    qryset.values()

look up fields in a related model/table (i.e. join)
connect the field in the current model to the desired field in the other model

    cls.values('species_key','image_key__image')
