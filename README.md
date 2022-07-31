### PRP

# 주제 소개

PRP(for your portrait right protection)

업로드 할 당신의 영상 속 인물들의 초상권을 보호할 수 있도록 이 서비스를 이용해보세요

사용자는 업로드 할 영상 속 특정 인물만을 지정하여 모자이크 처리와 캐릭터 변환 처리를 실행할 수 있고 이를 통한 안전한 영상 업로드가 가능할 것 입니다.

서비스 이용방법은 정말 쉽습니다. 사이트에서 회원가입을 한 후, 초상권을 보호하지 않을 인물의 사진을 업로드 합니다. 초상권 보호를 위한 영상을 업로드하고 모자이크과 케릭터 사진 중 어느 것으로 초상권 보호를 할지 선택하면 끝입니다. 당신은 이 서비스에서 당신만의 케릭터를 추가할 수 있고, 당신이 초상권 보호에서 제외할 사람들의 명단과 사진들을 관리할 수 있습니다. 물론, 당신이 수정한 비디오 또한 확인할 수 있습니다.

당신이 이 서비스를 유용하게 이용하면 좋겠습니다. 감사합니다!

# 소개영상

(향후 데모영상 삽입)

# 소프트웨어 아키텍처

![Untitled](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/0772fde4-8afb-4f84-b049-724878e80282/Untitled.png)

# 기술스택 - 각 포지션별로

## **⚡ Tech Stack**

 `Frontend: React`

`- Backend : Flask, flask_restx, flask_mongoenginee, flask_migrate, flask_cors
- Web Server: Nginx
- WSGI: Gunicorn
- Database: MongoDB
- AI : Tensorflow, OpenCV, Colab
- Deployment: Docker, AWS EC2, AWS S3
-API Test : Postman
-API Documentation : Swagger`

`-version control: Git, Github, Gitkraken`

Development Environment : Visual studio code, colab

# start 방법

```
$ cd “YOUR_DOWNLOAD_LOCATION”

$ git clone 울팀 주소
**(향후 docker-compose단계에서 yarn명령어 추가하기)**
```

backend 폴더에 당신이 수정해야할 몇가지 파일이 있습니다. (향후 아래 내용으로 파일 추가하기)

buket/

m_config.py

```python
AWS_ACCESS_KEY = "YOUR_AWS_ACCESS_KEY"
AWS_SECRET_ACCESS_KEY = "YOUR_AWS_SECRET_ACCESS_KEY"
AWS_S3_BUCKET_REGION = "YOUR_AWS_S3_BUCKET_REGION"
AWS_S3_BUCKET_NAME = "YOUR_AWS_S3_BUCKET_NAME"
AWS_S3_BUCKET_URL = "YOUR_AWS_S3_BUCKET_URL"
```

db/

db_config.py

```python
HOST = 'db'
PORT = 27017
```

module/

module_config.py

```python
SECRET_KEY = "YOUR_TOKEN_SECRET_KEY"
TOKEN_EXPIRED = 3600 #3600 sec, If you want longer, you can change this time.
```

```
$ docker-compose up --build
```

# 팀원 역할

| Name    | 박수현                                       |정태원                               | 박수연                                        | 조성현      | 이민지 | 박준혁                              |
| ------- | --------------------------------------------- | ------------------------------------ | --------------------------------------------- | --------------------------------------- | -----| ----- |
| Role    |     Backend    |             Frontend          |     Backend       | Frontend | Frontend | Backend  |
| Github  | [@vivian0304](https://github.com/vivian0304) | [@teawon](https://github.com/teawon) | [@PARK-Su-yeon](https://github.com/PARK-Su-yeon) | [@vixloaze](https://github.com/vixloaze) | [@alswlfl29](https://github.com/alswlfl29)| [@JHPark02](https://github.com/JHPark02)|
