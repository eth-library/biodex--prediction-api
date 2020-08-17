#!/bin/bash

# # podman create network
POD_NAME=biodex_web

#create directories if not already existing
VOL_DIR=~/volumes/web
VOL_NGINX=$VOL_DIR/nginx
VOL_MEDIA=$VOL_DIR/mediafiles
VOL_STATIC=$VOL_DIR/staticfiles
VOL_DB=$VOL_DIR/postgres
VOL_FIXT=$VOL_DIR/fixturefiles

mkdir -p -v $VOL_MEDIA
mkdir -p -v $VOL_STATIC
mkdir -p -v $VOL_DB
mkdir -p -v $VOL_FIXT

# get these from environment variables when finished debugging
# define host ports for services
PORT_PROXY_HOST=$(grep -Eo '(^PORT_PROXY_HOST=)([0-9]+)' .env.prod | grep -Eo '[0-9]+')

# define container ports for services
PORT_PROXY_CTR=80
PORT_DB_CTR=5432
PORT_WEB_CTR=7000
PORT_TF_CTR=8501

podman pod create \
    -p $PORT_PROXY_HOST:$PORT_PROXY_CTR \
    -n $POD_NAME
# DATABASE
CTR_NAME=biodex_db-prod-ctr
echo "running $CTR_NAME"
podman run \
    --name $CTR_NAME \
    --pod $POD_NAME \
    -d \
    --env-file .env.prod.db \
    --volume $VOL_DB:/var/lib/postgresql/data/ \
    --restart always \
    postgres:12.0-alpine

# PREDICTION MODEL
CTR_NAME=biodex_tf-prod-ctr
echo "running $CTR_NAME"
podman run \
    --name $CTR_NAME \
    -d \
    --pod $POD_NAME \
    --restart always \
    biodex/prediction_model:201911171137


CTR_NAME_WEB=biodex_webapp-prod-ctr
echo "running $CTR_NAME_WEB"
podman run \
    --name  $CTR_NAME_WEB \
    --pod $POD_NAME \
    -d \
    --volume $VOL_STATIC:/home/app/web/staticfiles:z \
    --volume $VOL_MEDIA:/home/app/web/mediafiles:z \
    --volume $VOL_FIXT:/home/app/web/fixturefiles \
    --env-file .env.prod \
    --restart always \
    biodex/webapp-prod-img:20200812 \
    gunicorn backend.wsgi:application --bind 127.0.0.1:$PORT_WEB_CTR


#REVERSE PROXY
CTR_NAME=biodex_nginx-prod-ctr
echo "running $CTR_NAME"
podman run \
    --name $CTR_NAME \
    -d \
    --pod $POD_NAME \
    --volume $VOL_NGINX:/etc/nginx/conf.d \
    --volume $VOL_STATIC:/data/staticfiles:ro \
    --volume $VOL_MEDIA:/data/mediafiles:ro \
    --restart always \
    nginx:1


echo 'making migrations'
podman exec -d $CTR_NAME_WEB python manage.py makemigrations
echo 'migrating'
podman exec -d $CTR_NAME_WEB python manage.py migrate
echo 'collecting static files'
podman exec -d $CTR_NAME_WEB python manage.py collectstatic --no-input

# need to manually create a superuser and then load fixture files
# podman exec -it $CTR_NAME_WEB python manage.py createsuperuser

# # #'loading fixtures'
# podman exec $CTR_NAME_WEB sh load_fixtures.sh