#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
    "Waiting for $DATABASE to start..."

    sleep 5
    
    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep .5
    done

    echo "$DATABASE has started"
fi


# python manage.py flush --no-input
python manage.py migrate
python manage.py collectstatic --no-input --clear

exec "$@"