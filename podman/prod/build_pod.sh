# podman create network
mkdir -p biodex

podman pod create -p 7000 -n biodex_web

# run web app
# podman run [flags] IMAGE [COMMAND [ARG...]]

# DATABASE
podman run \
    --name biodex_db-prod-ctr \
    --pod biodex_web \
    --expose 7020 \
    -p 7010:7010 \
    -d \
    --env-file .env.prod.db \
    --volume biodex/postgres_data:/var/lib/postgresql/data/ \
    --restart always \
    postgres:12.0-alpine

#PREDICTION MODEL
podman run \ 
    --name biodex_tf-prod-ctr \
    --expose 7030
    biodex/prediction_model:201911171137 \ #IMAGE

#REVERSE PROXY
podman run \
    --name biodex_nginx-prod-ctr \
    -p 7000:80
    --volume ~vol_mount/biodex/media_volume:/home/app/web/mediafiles
    nginx:1.17.4-alpine

# # PREDICTION API & WEBSITE
# podman run \
#     --name biodex_webapp-prod-ctr \ #container name
#     --pod biodex-web \ # name of pod to add container to
#     -p 7000:7000 \ # publish/map this container port to the host
#     -d \ # detached mode
#     --env-file .env.prod \ # load env variables from this file
#     --volume biodex/static_volume:/home/app/web/staticfiles \ # mount this volume from host to container
#     --volume biodex/media_volume:/home/app/web/mediafiles \ # mount this volume from host to container
#     --restart always \
#     biodex/webapp-prod-img \ # IMAGE to run
#     gunicorn backend.wsgi:application --bind 0.0.0.0:7000\ # COMMAND to run upon start


