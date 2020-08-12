
#cd to project root
cd ../../
ROOT_DIR=$PWD

echo "building gunicorn-Django image"
cd $ROOT_DIR/app
buildah bud -t biodex/webapp-dev-img -f ./Dockerfile

echo "building nginx image"
cd $ROOT_DIR/nginx
buildah bud -t biodex/nginx-prod-img -f ./Dockerfile

echo "pulling postgres image"
podman pull postgres:12.0-alpine

echo "pulling prediction_model image"
podman pull biodex/prediction_model

