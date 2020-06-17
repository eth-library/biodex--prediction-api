#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
    "Waiting for $DATABASE to start..."

    sleep 5 # using while loop with nc (netcat) and mysqladmin fails as packages are not found
    
    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep .5
    done

    echo "assuming $DATABASE has started"
fi


# python manage.py flush --no-input
# python manage.py migrate
# python manage.py collectstatic --no-input --clear
# python3 manage.py createsuperuser --no-input username=$DJANGO_SUPERUSER_USERNAME password=$DJANGO_SUPERUSER_PASSWORD EmailField=$DJANGO_SUPERUSER_EMAIL

exec "$@"