#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for $DATABASE to start..."

    sleep 5 
    
    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep .5
    done

    echo "$DATABASE has started"
fi

exec "$@"
