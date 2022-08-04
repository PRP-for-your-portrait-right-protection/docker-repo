# <img style="width: 45px; height: 50px" src="https://user-images.githubusercontent.com/93627156/182650226-66ba6885-dbf0-494f-8047-50f2992bf48d.png"/> PRP(for your portrait right protection)
[English](https://github.com/PRP-for-your-portrait-right-protection/docker-repo/blob/develop/README.md) | **한국어**

# 주제 소개


업로드 할 당신의 영상 속 인물들의 초상권을 보호할 수 있도록 이 서비스를 이용해보세요

사용자는 업로드 할 영상 속 특정 인물만을 지정하여 모자이크 처리와 캐릭터 변환 처리를 실행할 수 있고 이를 통한 안전한 영상 업로드가 가능할 것 입니다.

서비스 이용방법은 정말 쉽습니다. 사이트에서 회원가입을 한 후, 초상권을 보호하지 않을 인물의 사진을 업로드 합니다. 초상권 보호를 위한 영상을 업로드하고 모자이크과 케릭터 사진 중 어느 것으로 초상권 보호를 할지 선택하면 끝입니다. 당신은 이 서비스에서 당신만의 케릭터를 추가할 수 있고, 당신이 초상권 보호에서 제외할 사람들의 명단과 사진들을 관리할 수 있습니다. 물론, 당신이 수정한 비디오 또한 확인할 수 있습니다.

당신이 이 서비스를 유용하게 이용하면 좋겠습니다. 감사합니다!

# 소개영상

(향후 데모영상 삽입)

# 소프트웨어 아키텍처

![image](https://user-images.githubusercontent.com/93627156/182640860-7ba4d408-dd70-4bdd-a45b-7adc4f7bee2d.png)

# 기술스택 - 각 포지션별로
## **:zap: Tech Stack**
```
- Frontend: React, nodejs, javascript, typescript
- Backend : Flask, flask_restx, flask_mongoenginee
- Web Server: Nginx
- WSGI: Gunicorn
- Database: MongoDB
- AI : Numpy, pillow, dlib, OpenCV, Colab
- Deployment: Docker, AWS EC2, AWS S3
- API Test : Postman
- API Documentation : Swagger
- Version control: Git, Github, Gitkraken
- Development Environment : Visual studio code, colab
```
|Frontend|Backend|AI|DevOps|Other|
|:------:|:------:|:---:|:----:|:---:|
|![JavaScript](https://img.shields.io/badge/javascript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)<br>![TypeScript](https://img.shields.io/badge/typescript-3178C6?style=for-the-badge&logo=typescript&logoColor=black)<br>![React](https://img.shields.io/badge/react-%2320232a.svg?style=for-the-badge&logo=react&logoColor=%2361DAFB)<br>![NodeJS](https://img.shields.io/badge/node.js-%2343853D.svg?style=for-the-badge&logo=node.js&logoColor=white)|![Python](https://img.shields.io/badge/python-%2314354C.svg?style=for-the-badge&logo=python&logoColor=white)<br>![Flask](https://img.shields.io/badge/Flask-black.svg?style=for-the-badge&logo=Flask&logoColor=white)<br>![MongoDB](https://img.shields.io/badge/MongoDB-%234ea94b.svg?style=for-the-badge&logo=mongodb&logoColor=white)<br>![gunicorn](https://img.shields.io/badge/gunicorn-499848?style=for-the-badge&logo=gunicorn&logoColor=white)<br>|![dlib](https://img.shields.io/badge/dlib-darkgreen.svg?style=for-the-badge&logo=dlib&logoColor=white)</br>![numpy](https://img.shields.io/badge/numpy-013243?style=for-the-badge&logo=numpy&logoColor=white)<br>![OpenCV](https://img.shields.io/badge/opencv-%23white.svg?style=for-the-badge&logo=opencv&logoColor=white)|![Colab](https://img.shields.io/badge/colab-%F9AB00.svg?style=for-the-badge&logo=googlecolab&logoColor=white)</br>![Nginx](https://img.shields.io/badge/nginx-%23009639.svg?style=for-the-badge&logo=nginx&logoColor=white)<br>![AWS](https://img.shields.io/badge/AWS-%23FF9900.svg?style=for-the-badge&logo=amazon-aws&logoColor=white)<br>![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)|![Postman](https://img.shields.io/badge/Postman-FF6C37?style=for-the-badge&logo=Postman&logoColor=white)<br>![Git](https://img.shields.io/badge/git-%23F05033.svg?style=for-the-badge&logo=git&logoColor=white)<br>![GitHub](https://img.shields.io/badge/github-%23121011.svg?style=for-the-badge&logo=github&logoColor=white)<br>![Visual Studio Code](https://img.shields.io/badge/VisualStudioCode-0078d7.svg?style=for-the-badge&logo=visual-studio-code&logoColor=white)<br>![Slack](https://img.shields.io/badge/Slack-4A154B?style=for-the-badge&logo=slack&logoColor=white)<br>![Notion](https://img.shields.io/badge/Notion-%23000000.svg?style=for-the-badge&logo=notion&logoColor=white)

# start 방법

```
cd “YOUR_DOWNLOAD_LOCATION”

git clone --recursive https://github.com/PRP-for-your-portrait-right-protection/docker-repo.git

## insert configFile (m_config.py , module_config.py)

docker-compose -f docker-compose.yml up -d --build

```

### Setting File


- docker-repo/backend-repo/bucket/m_config.py
- docker-repo/celery-repo/bucket/m_config.py

```python
AWS_ACCESS_KEY = "YOUR_AWS_ACCESS_KEY"
AWS_SECRET_ACCESS_KEY = "YOUR_AWS_SECRET_ACCESS_KEY"
AWS_S3_BUCKET_REGION = "YOUR_AWS_S3_BUCKET_REGION"
AWS_S3_BUCKET_NAME = "YOUR_AWS_S3_BUCKET_NAME"
AWS_S3_BUCKET_URL = "YOUR_AWS_S3_BUCKET_URL"
```




- docker-repo/backend-repo/module/module_config.py 

```python
SECRET_KEY = "YOUR_TOKEN_SECRET_KEY"
TOKEN_EXPIRED = 3600 #3600 sec, If you want longer, you can change this time.
```



# 팀원 역할

| Name    | 박수현                                       |정태원                               | 박수연                                        | 조성현      | 이민지 | 박준혁                              |
| ------- | --------------------------------------------- | ------------------------------------ | --------------------------------------------- | --------------------------------------- | -----| ----- |
| Role    |     Backend    |             Frontend          |     Backend       | Frontend | Frontend | Backend  |
| Github  | [@vivian0304](https://github.com/vivian0304) | [@teawon](https://github.com/teawon) | [@PARK-Su-yeon](https://github.com/PARK-Su-yeon) | [@vixloaze](https://github.com/vixloaze) | [@alswlfl29](https://github.com/alswlfl29)| [@JHPark02](https://github.com/JHPark02)|
