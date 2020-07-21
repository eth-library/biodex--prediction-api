# Containerization with Podman

As podman does not have a mature equivalent to docker-compose, we will create a script to execute the steps necessary for starting the container services. 
These involve
1. build required images with buildah
1. create a network (a pod) to hold the containers
1. add containers to the pod using the prebuilt images and the environment variables file

## Build Images

custom images are either built using a Dockerfile or downloaded directly from a container registry (e.g. docker hub) 

* django web app

    create directories when building image

    /home/app/web/..
        ..staticfiles
        ..mediafiles
        ..fixturefiles

    copy all code and static files into image during build
    dockerignore prevents copying media files
    mount media volume when running containing

        mediafiles

