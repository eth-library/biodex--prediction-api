CTR_LIST="biodex_webapp-dev-ctr biodex_db-dev-ctr biodex_tf-dev-ctr biodex_nginx-dev-ctr"
echo "attempting to stop containers"
for CTR in $CTR_LIST; do
    podman stop $CTR
done

echo "attempting to remove containers"
for CTR in $CTR_LIST; do
    podman rm $CTR;
done

echo "stopping pod"
podman pod stop biodex_web_dev
echo "removing pod"
podman pod rm biodex_web_dev
