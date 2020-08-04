# Taxonomic Terminology

#### binomial naming

species are named using the binomial format where the combination of the Genus and specific epithet define a species, e.g. Homo sapiens. 

#### sp.
sp. is used when the genus can be identified but the exact species cannot or does not need to be determined. e.g. Homo sp. refers to some unidentified species of the genus Homo.

# Copyright

When using images from other people/collections/entities it is very important to ensure that 
we have permission to distribute the images.

Attribution-NonCommercial-ShareAlike 3.0 Unported (CC BY-NC-SA 3.0)
http://creativecommons.org/licenses/by-nc-sa/3.0/

# Main Deployment Steps

1. log in to server & pull codebase from remote git repo
1. save local prediction docker image as tar file, transfer to server and load with docker
1. transfer image, fixturefile &  staticfile tar files to server
1. transfer env variable files
1. run docker-compose -f docker-compose.prod.yml -p biodex up --build
1. run migrations to tables: migrate docker-compose -f docker-compose.prod.yml exec web python manage.py migrate
1. create superuser for django
1. load fixture files using bash script: docker-compose exec web sh load_fixtures.sh 

## save local docker image and transfer to server

save docker image as a tar file

<p>

    docker save -o <path to generated file.tar> <image name>

</p>

Then copy your image to the host server with regular file transfer tools such as cp, scp.  
Then load the image into Docker:

    docker load -i <path to image tar file>

# Rebuild and Run for Production

generate new secret keys

<p>

    from django.core.management.utils import get_random_secret_key

    print(get_random_secret_key())

</p>

remove volumes and stop running containers

<p>

    
    docker-compose down -v
</p>

build the images (--build), start the containers and run in background ie no console logging (-d)  

<p>

    docker-compose -f docker-compose.prod.yml up -d --build

</p>

in the web container, run migrations with django  

<p>

    docker-compose -f docker-compose.prod.yml exec web python manage.py migrate --noinput

</p>

collect any static files

<p>

    docker-compose -f docker-compose.prod.yml exec web python manage.py collectstatic --no-input --clear

</p>

if needed, open an interactive shell on a running container

<p>

    docker exec -it <container-number> /bin/bash

</p>


copy a file into a container

<p>
    docker cp ./biodex_logo.svg 4627ca15283b:/usr/src/app/staticfiles/images/biodex_logo.svg
</p>
create a admin/superuser in the django app

<p>

    docker-compose -f docker-compose.prod.yml exec web python manage.py createsuperuser

</p>


load fixture files using the convenience bash script

<p>

    docker-compose exec web sh load_fixtures.sh

</p>


connect to an interactive shell for the postgres database

<p>

    docker-compose exec db psql --username=admin --dbname=biodex_dev

</p>

## Check
    Upload an image at http://localhost:52500/.
    Then, view the image at http://localhost:1337/mediafiles/IMAGE_FILE_NAME

# Dockerizing Django with Postgres, Gunicorn, and Nginx
https://github.com/testdrivenio/django-on-docker

## Want to learn how to build this?

Check out the [post](https://testdriven.io/dockerizing-django-with-postgres-gunicorn-and-nginx).

## Want to use this project?



# Prediction Model

 
## Embed model in a Docker Image 
__(reference https://www.tensorflow.org/tfx/serving/docker)__  

make sure that the model that you want to containerize is saved in the models folder in the model_serving directory. The model should be in the tf.saved_model format, with a numerical folder name (e.g. a datetimestamp 202004281030)

Go to model_serving folder and run:

    bash make_docker_image.sh

this convenience script pulls the tensorflow serving base image, adds the selected model from the local models folder, and creates a new image tagged with latest & the model number (see Dockerfile for more details

## run the container
docker run -p 8501:8501 [DOCKER_IMAGE_NAME]

#this exposes an endpoint that can be used for predictions

SERVER_URL = 'http://localhost:8501/v1/models/[DOCKER_IMAGE_NAME]:predict'


## things that are needed by the model for predictions

  
### variables that change with every model


#### image normalization values

before the image is sent to the tensorflow model for prediction, the rgb values in the image are normalized, using the mean values for rgb mean and rgb standard deviation which was calculated for that model's training data. 

#### species_key_map
maps the species as numbered by the prediction model, to the species PKs in the database
model classes will range from 0 to n, where _n_ is the number species the model was trained on. Class 0 in one model may not be the same as class 0 in a different model.The individual model ids need to be mapped to permanent species id numbers in the db

* __encoded hierarchy maps__

this maps how classes in each hierarchical level map to the classes in their parent level. This is used when summing up the probabilies from the species level up to the family level.


# Authentication
__Uses Djoser__

list of available endpoints
https://djoser.readthedocs.io/en/latest/getting_started.html#available-endpoints


### create user
http://127.0.0.1:8000/api/auth/users/

### request token

http://127.0.0.1:8000/api/auth/token/login/


# Example Curl Requests

## Request Token
curl -X POST -d '{"username": "admin","password": "1234"}' -H 'Content-Type: application/json'  http://127.0.0.1:8000/api/auth/token/login/

## Using  Token 
curl -X POST http://127.0.0.1:8000/api/predict/ -H 'Authorization: Token a21e26bd12a16542f940d641e840e32ad16a26d0' [{"id":1,"name":"admin"]