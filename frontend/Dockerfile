#FROM node:16.10.0
FROM node:latest

USER root 
#USER : 명령을 실행하기 위한 특정 사용자를 지정하는 부분  (환경 설정 권한 등)


WORKDIR /frontend
COPY . /frontend

# Make variable API_URL to put uri into url
# uri 변수 형태로 받아서 url에 넣어 작동하도록 함
ENV REACT_APP_HOST_IP_ADDRESS $API_URL
ENV REACT_APP_BACKEND_URL $REACT_APP_BACKEND_URL
#ENV : react사용을 할 때 환경변수와 관련된 설정


RUN yarn --ignore-platform
#COPY . ./
# 빼도 될 것 같습니다

# build file을 개발용에서는 불러오지 않기 때문에 개발용에서는 npm start 가능
RUN yarn run build
