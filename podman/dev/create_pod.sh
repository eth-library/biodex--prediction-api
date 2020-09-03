#!/bin/bash

# # podman create network
POD_NAME=biodex_web_dev
echo "creating pod: $biodex_web_dev"

#create directories if not already existing
VOL_DIR=~/biodex/dev/volumes
VOL_NGINX=$VOL_DIR/nginx
VOL_MEDIA=$VOL_DIR/mediafiles
VOL_STATIC=$VOL_DIR/staticfiles
VOL_DB=$VOL_DIR/postgres
VOL_FIXT=$VOL_DIR/fixturefiles
VOL_CODE=~/projects/api/app

mkdir -p -v $VOL_NGINX
mkdir -p -v $VOL_MEDIA
mkdir -p -v $VOL_STATIC
mkdir -p -v $VOL_DB
mkdir -p -v $VOL_FIXT

# copy nginx config
cp -i -v ./nginx-dev.conf $VOL_NGINX/nginx-dev.conf

# get these from environment variables when finished debugging
# define host ports for services
PORT_PROXY_HOST=8000
PORT_DB_HOST=8010
PORT_WEB_HOST=8020
PORT_TF_HOST=8030

# define container ports for services
PORT_PROXY_CTR=80
PORT_DB_CTR=5432
PORT_WEB_CTR=7000
PORT_TF_CTR=8501

podman pod create \
    -p $PORT_PROXY_HOST:$PORT_PROXY_CTR \
    -p $PORT_WEB_HOST:$PORT_WEB_CTR \
    -p $PORT_DB_HOST:$PORT_DB_CTR \
    -p $PORT_TF_HOST:$PORT_TF_CTR \
    -n $POD_NAME

# DATABASE
CTR_NAME=biodex_db-dev-ctr
echo "running $CTR_NAME"
podman run \
    --name $CTR_NAME \
    --pod $POD_NAME \
    -p $PORT_DB_HOST:$PORT_DB_CTR \
    -d \
    --env-file .env.dev.db \
    --volume $VOL_DB:/var/lib/postgresql/data/ \
    --restart always \
    postgres:12.0-alpine

# PREDICTION MODEL
CTR_NAME=biodex_tf-dev-ctr
echo "running $CTR_NAME"
podman run \
    --name $CTR_NAME \
    -d \
    --pod $POD_NAME \
    -p $PORT_TF_HOST:$PORT_TF_CTR \
    biodex/prediction_model:201911171137

#web app
# CTR_NAME_WEB=biodex_webapp-prod-ctr
# echo "running $CTR_NAME_WEB"
# podman run \
#     --name  $CTR_NAME_WEB \
#     --pod $POD_NAME \
#     -d \
#     --volume ~/biodex/volumes/staticfiles:/home/app/web/staticfiles \
#     --volume ~/biodex/volumes/mediafiles:/home/app/web/mediafiles \
#     --volume ~/biodex/volumes/fixturefiles:/home/app/web/fixturefiles \
#     --env-file .env.prod \
#     --restart always \
#     biodex/webapp-prod-img \
#     gunicorn backend.wsgi:application --bind 0.0.0.0:7000



CTR_NAME_WEB=biodex_webapp-dev-ctr
echo "running $CTR_NAME_WEB"
podman run \
    --name  $CTR_NAME_WEB \
    --pod $POD_NAME \
    -d \
    --volume $VOL_CODE:/home/app/web/ \
    --volume $VOL_STATIC:/home/app/web/staticfiles \
    --volume $VOL_MEDIA:/home/app/web/mediafiles \
    --volume $VOL_FIXT:/home/app/web/fixturefiles \
    --env-file .env.dev \
    localhost/biodex/webapp-dev-img \
    gunicorn backend.wsgi:application --bind 0.0.0.0:$PORT_WEB_CTR --reload


# podman run \
#     --name biodex_webapp-dev-ctr \
#     --pod biodex_web_dev \
#     --volume ~/projects/api/app:/home/app/web/:ro \
#     --volume ~/biodex_dev/volumes/staticfiles:/home/app/web/staticfiles \
#     --volume ~/biodex_dev/volumes/mediafiles:/home/app/web/mediafiles \
#     --volume ~/biodex_dev/volumes/fixturefiles:/home/app/web/fixturefiles \
#     --env-file .env.dev \
#     localhost/biodex/webapp-dev-img \
#     python manage.py runserver 7000
#     # gunicorn backend.wsgi:application --bind 0.0.0.0:7000


#REVERSE PROXY
CTR_NAME=biodex_nginx-dev-ctr
echo "running $CTR_NAME"
podman run \
    --name $CTR_NAME \
    -d \
    --pod $POD_NAME \
    -p $PORT_PROXY_HOST:$PORT_PROXY_CTR \
    --volume $VOL_NGINX:/etc/nginx/conf.d:ro \
    --volume $VOL_STATIC:/data/staticfiles:ro \
    --volume $VOL_MEDIA:/data/mediafiles:ro \
    nginx:1

echo 'making migrations'
podman exec -d $CTR_NAME_WEB python manage.py makemigrations
echo 'migrating'
podman exec -d $CTR_NAME_WEB python manage.py migrate
echo 'collecting static files'
podman exec -d $CTR_NAME_WEB python manage.py collectstatic --no-input

# automatically create a superuser for test purposes

# podman exec -it $CTR_NAME_WEB python manage.py createsuperuser
# echo "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@example.com', 'password')" | podman exec -it $CTR_NAME_WEB python web/manage.py shell

# # #'loading fixtures'
# podman exec $CTR_NAME_WEB sh load_fixtures.sh