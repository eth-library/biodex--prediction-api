# Rebuild and Run for Production

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

create a admin/superuser in the django app

<p>

    docker-compose -f docker-compose.prod.yml exec web python manage.py createsuperuser

</p>


## Check
    Upload an image at http://localhost:1337/.
    Then, view the image at http://localhost:1337/mediafiles/IMAGE_FILE_NAME

# Dockerizing Django with Postgres, Gunicorn, and Nginx
https://github.com/testdrivenio/django-on-docker

## Want to learn how to build this?

Check out the [post](https://testdriven.io/dockerizing-django-with-postgres-gunicorn-and-nginx).

## Want to use this project?

### Development

Uses the default Django development server.

1. Rename *.env.dev-sample* to *.env.dev*.
1. Update the environment variables in the *docker-compose.yml* and *.env.dev* files.
1. Build the images and run the containers:

    ```sh
    $ docker-compose up -d --build
    ```

    Test it out at [http://localhost:8000](http://localhost:8000). The "app" folder is mounted into the container and your code changes apply automatically.

### Production

Uses gunicorn + nginx.

1. Rename *.env.prod-sample* to *.env.prod* and *.env.prod.db-sample* to *.env.prod.db*. Update the environment variables.
1. Build the images and run the containers:

    ```sh
    $ docker-compose -f docker-compose.prod.yml up -d --build
    ```

    Test it out at [http://localhost:1337](http://localhost:1337). No mounted folders. To apply changes, the image must be re-built.



# MODEL 
## updates
_things that change with every new model_

* __model class numbers__  

    model classes will range from 0 to the number species the model was trained on. Class 0 in one model may not be the same as class 0 in a different model.  
    The individual model ids need to be mapped to permanent species id numbers

* __class hierarchy maps__

    
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

