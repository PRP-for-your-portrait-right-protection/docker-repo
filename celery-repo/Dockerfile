#FROM python:3.7.7
#FROM tensorflow/tensorflow:latest-gpu
FROM --platform=linux/x86_64 python:3.7

RUN mkdir /celery
WORKDIR /celery

COPY . /celery/

RUN pip install --upgrade pip
# RUN pip3 install tensorflow
RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6  -y
RUN pip install -r requirements.txt
RUN pip install cmake
RUN pip3 install dlib

ENTRYPOINT celery -A tasks worker --loglevel=info