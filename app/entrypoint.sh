#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting 15s for $DATABASE to start..."

    sleep 15 # using while loop with nc (netcat) and mysqladmin fails as packages are not found
    
    # while ! nc -z $SQL_HOST $SQL_PORT; do
    # while ! mysqladmin ping -h"$SQL_HOST" --silent; do
      # sleep .5
    # done

    echo "assuming $DATABASE has started"
fi


python manage.py flush --no-input
python manage.py migrate
python manage.py collectstatic --no-input --clear
python3 manage.py createsuperuser

exec "$@"