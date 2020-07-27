# pull official base image
FROM python:3.8.3-alpine


ENV HOME=/home/app
ENV APP_HOME=/home/app/web
# set work directory
WORKDIR $HOME

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
# install psycopg2 dependencies
RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev \
    # needed for Pillow
    && apk add jpeg-dev zlib-dev libjpeg 

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt $HOME/requirements.txt
RUN pip install -r requirements.txt

# Mount a Volume to allow live updates
VOLUME $APP_HOME
WORKDIR $APP_HOME
