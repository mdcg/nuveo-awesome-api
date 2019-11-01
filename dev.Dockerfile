FROM python:3.6.9-alpine3.10

MAINTAINER MDCG
ENV PYTHONUNBUFFERED 1
ENV DJANGO_ENV dev
ENV DOCKER_CONTAINER 1

RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev jpeg-dev zlib-dev

COPY ./requirements.txt /code/requirements.txt
RUN pip install -r /code/requirements.txt

COPY . /code/
WORKDIR /code/

EXPOSE 8000
