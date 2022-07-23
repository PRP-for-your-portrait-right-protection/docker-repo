FROM python:latest

RUN mkdir /celery
WORKDIR /celery

COPY . /celery/

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# 컨테이너가 수행될 때 변경되지 않을 실행 명령은 CMD 보다는 ENTRYPOINT로 정의하는게 좋다.
ENTRYPOINT celery -A tasks worker --loglevel=info