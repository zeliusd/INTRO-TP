# syntax=docker/dockerfile:1

FROM python:3.8-slim-buster

WORKDIR /api/

RUN pip3 install --upgrade pip

COPY . /api/.

RUN pip3 install -r dependencias.txt

RUN apt update

RUN apt install -y unzip 

ENTRYPOINT [ "/api/entrypoint.sh" ]

