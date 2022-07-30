import numpy as np
import cv2
import moviepy.editor as mp #소리 추출
#--------
# 라이브러리
import dlib
import matplotlib.pyplot as plt
from PIL import ImageFont, ImageDraw, Image
import tensorflow.keras 
from tensorflow.keras import backend as K
import time
import ffmpeg
# 셀러리
from celery import Celery
from celery.utils.log import get_task_logger
import time
####
import boto3
from m_config import AWS_ACCESS_KEY, AWS_SECRET_ACCESS_KEY, AWS_S3_BUCKET_NAME, AWS_S3_BUCKET_REGION, AWS_S3_BUCKET_URL
import os
import shutil
from datetime import datetime

logger = get_task_logger(__name__)

# app = Celery('tasks',
#     broker='amqp://localhost:5672',
#     result_backend='mongodb://localhost:27017/',
#     mongodb_backend_settings = {
#         'database': 'silicon',
#         'taskmeta_collection': 'celery'
#     }
# )
app = Celery('tasks',
    broker='amqp://admin:mypass@rabbitmq:5672',
    result_backend='mongodb://db:27017/',
    mongodb_backend_settings = {
        'database': 'silicon',
        'taskmeta_collection': 'celery'
    }
)

def find_faces(img):
    detector = dlib.get_frontal_face_detector()
    sp = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')
    dets = detector(img, 1)
    
    if len(dets) == 0:
        return np.empty(0), np.empty(0), np.empty(0)
    
    rects, shapes = [], []
    shapes_np = np.zeros((len(dets), 68, 2), dtype=np.int)
    for k, d in enumerate(dets):
        rect = ((d.left(), d.top()), (d.right(), d.bottom()))
        rects.append(rect)

        shape = sp(img, d)
        
        # convert dlib shape to numpy array
        for i in range(0, 68):
            shapes_np[k][i] = (shape.part(i).x, shape.part(i).y)

        shapes.append(shape)
        
    return rects, shapes, shapes_np

# 랜드마크 추출
def encode_faces(img, shapes):
    facerec = dlib.face_recognition_model_v1('dlib_face_recognition_resnet_model_v1.dat')
    face_descriptors = []
    for shape in shapes:
        face_descriptor = facerec.compute_face_descriptor(img, shape)
        face_descriptors.append(np.array(face_descriptor))

    return np.array(face_descriptors)

# 모자이크
@app.task()
def mosaic(whitelistFaceImgList, videoUrl, user):
    logger.info('Got Request - Starting work ')
    logger.info(whitelistFaceImgList)
    logger.info(videoUrl)
    logger.info(user)

    # 유저 이름으로 폴더 생성 (폴더가 존재하지 않는 경우에 생성)
    if not os.path.isdir(user):
        os.mkdir(user)

    img_paths = whitelistFaceImgList   

    descs = []
    name = ""

    count = 0 
    new_img_paths = []
    for img_path in img_paths:
        os.system("curl " + img_path + f' > {user}/{count}.jpg')
        img_paths[img_paths.index(img_path)] = f' > {user}/{count}.jpg'
        new_img_paths.append(f'{user}/{count}.jpg')
        count += 1

    for img_path in new_img_paths: # .items(): <---- key value 쌍 얻기
        img = cv2.imread(img_path)
        _, img_shapes, _ = find_faces(img)
        descs.append([name, encode_faces(img, img_shapes)[0]])
        
    np.save(f'{user}/descs.npy', descs)

    #url = 'https://www.youtube.com/watch?v=S_0ikqqccJs' #url 링크 (추후 사용자로부터 입력받은 영상파일 && 옵션에 따라 실시간 영상처리)
    #video = pafy.new(url)

    #best = video.getbest(preftype="mp4")

    os.system("curl " + videoUrl + f' > {user}/before.mp4')
    cap = cv2.VideoCapture(f'{user}/before.mp4') #직접 영상 사용  ##입력받은 영상의 url?을 넣습니다. 이부분도 props로 받아서 넣어주어야해요.
    ##cap = cv2.VideoCapture(0) # 노트북 웹캠을 카메라로 사용 

    xml = "haarcascade_frontalface_default.xml" #얼굴인식과 관련된 xml , 정확도가 떨어져서 이 부분만 따로 학습시키거나 해야..?

    res=(int(cap.get(3)),int(cap.get(4))) #resulotion

    fourcc = cv2.VideoWriter_fourcc('m','p','4','v')
    out = cv2.VideoWriter(f'{user}/last.mp4', fourcc, 30.0, res) #저장할 영상의 파일 명  ##어떤파일명으로 저장할 지 정하지만 이 파일명은 최종이 아닙니다. 여기서 나온 결과물과 소리를 합성해야해요

    while True:
        # if(time.time() -  begin > 10):
        #  break
        ret, img = cap.read() 

        if not ret: #영상을 읽어올 수 없다면 종료
            break;
    

        rects, shapes, _ = find_faces(img) # 얼굴 찾기
        descriptors = encode_faces(img, shapes) # 인코딩
        
        for i, desc in enumerate(descriptors):
            x = rects[i][0][0] # 얼굴 X 좌표
            y = rects[i][0][1] # 얼굴 Y 좌표
            w = rects[i][1][1]-rects[i][0][1] # 얼굴 너비 
            h = rects[i][1][0]-rects[i][0][0] # 얼굴 높이
            
            # 추출된 랜드마크와 데이터베이스의 랜드마크들 중 제일 짧은 거리를 찾는 부분
            descs1 = sorted(descs, key=lambda x: np.linalg.norm([desc] - x[1]))
            dist = np.linalg.norm([desc] - descs1[0][1], axis=1)
            
            if dist < 0.45: # 그 거리가 0.45보다 작다면 그 사람으로 판단 
                name = descs1[0][0]
            else:  
                try:         # 0.45보다 크다면 모르는 사람으로 판단 -> 모자이크 처리
                    mosaic_img = cv2.resize(img[y:y+h, x:x+w], dsize=(0, 0), fx=0.04, fy=0.04) # 축소 # 캐릭터로 할 때 이부분 주석처리 하면 됨
                    mosaic_img = cv2.resize(mosaic_img, (w, h), interpolation=cv2.INTER_AREA)  # 확대
                    img[y:y+h, x:x+w] = mosaic_img # 인식된 얼굴 영역 모자이크 처리 
                except Exception as e:
                    continue;


            logger.info(datetime.now())
            # cv2.rectangle(img, (x, y), (x+w, y+h), (0,255,0), 2) # 얼굴 영역 박스 
        
        
        img = Image.fromarray(img)
        draw = ImageDraw.Draw(img)
        img = np.array(img)

        # cv2.imshow('result',img)
        # k = cv2.waitKey(10) & 0xff # 'ESC' 키 누르면 종료
        # if k == 27:
        #     break #나중에 삭제
            
        out.write(img)


    cap.release()
    out.release()

    cap_audio = mp.VideoFileClip(f'{user}/before.mp4')
    videoclip = mp.VideoFileClip(f'{user}/last.mp4')
    result = videoclip.set_audio(cap_audio.audio)

    temp = f'{user}_after_{datetime.now().strftime("%Y-%m-%d")}.mp4'

    result.write_videofile(f'{user}/{temp}', 
    codec='libx264', 
    audio_codec='aac', 
    temp_audiofile='temp-audio.m4a', 
    remove_temp=True)

    s3 = boto3.client(
            service_name='s3',
            region_name=AWS_S3_BUCKET_REGION,
            aws_access_key_id=AWS_ACCESS_KEY,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY
        )

    try:
        s3.upload_file(f'{user}/{temp}', AWS_S3_BUCKET_NAME, f'video/{temp}', ExtraArgs={'ACL':'public-read'}) 
    except Exception as e:
        print(e)
        return False

    location = f'{AWS_S3_BUCKET_URL}/video/{temp}'

    # 만들었던 폴더 삭제
    if os.path.exists(user):
        shutil.rmtree(user)

    logger.info('Work Finished ')

    return location

# @app.task()
# def character(whitelistFaceImgList, blockCharacterImgUrl, videoUrl, user):
#     # 유저 이름으로 폴더 생성 (폴더가 존재하지 않는 경우에 생성)
#     if not os.path.isdir(user):
#         os.mkdir(user)

#     img_paths = whitelistFaceImgList    #["user1.png"]

#     descs = []
#     name = ""

#     for img_path in img_paths: # .items(): <---- key value 쌍 얻기
#         img = cv2.imread(img_path)
#         _, img_shapes, _ = find_faces(img)
#         descs.append([name, encode_faces(img, img_shapes)[0]])
        
#     np.save("descs.npy", descs)




#     #url = 'https://www.youtube.com/watch?v=S_0ikqqccJs' #url 링크 (추후 사용자로부터 입력받은 영상파일 && 옵션에 따라 실시간 영상처리)
#     #video = pafy.new(url)

#     #best = video.getbest(preftype="mp4")

#     cap = cv2.VideoCapture(videoUrl) #직접 영상 사용  ##입력받은 영상의 url?을 넣습니다. 이부분도 props로 받아서 넣어주어야해요.
#     ##cap = cv2.VideoCapture(0) # 노트북 웹캠을 카메라로 사용 

#     xml = "haarcascade_frontalface_default.xml" #얼굴인식과 관련된 xml , 정확도가 떨어져서 이 부분만 따로 학습시키거나 해야..?

#     mosaic_img = cv2.imread('user1.png') #캐릭터 이미지로 변환 시 사용 ##변환시 사용하는 이미지입니다.

#     res=(int(cap.get(3)),int(cap.get(4))) #resulotion

#     # fourcc = cv2.VideoWriter_fourcc(*'DIVX') #codec
#     # out = cv2.VideoWriter('last.mp4', fourcc, 30.0, res) #저장할 영상의 파일 명  ##어떤파일명으로 저장할 지 정하지만 이 파일명은 최종이 아닙니다. 여기서 나온 결과물과 소리를 합성해야해요
#     fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
#     out = cv2.VideoWriter('last.mp4', fourcc, 30.0, res) #저장할 영상의 파일 명  ##어떤파일명으로 저장할 지 정하지만 이 파일명은 최종이 아닙니다. 여기서 나온 결과물과 소리를 합성해야해요

#     while True:
#         # if(time.time() -  begin > 10):
#         #  break
        
#         ret, img = cap.read() 

#         if not ret: #영상을 읽어올 수 없다면 종료
#             break;
    

#         rects, shapes, _ = find_faces(img) # 얼굴 찾기
#         descriptors = encode_faces(img, shapes) # 인코딩
        
#         for i, desc in enumerate(descriptors):
#             x = rects[i][0][0] # 얼굴 X 좌표
#             y = rects[i][0][1] # 얼굴 Y 좌표
#             w = rects[i][1][1]-rects[i][0][1] # 얼굴 너비 
#             h = rects[i][1][0]-rects[i][0][0] # 얼굴 높이
            
#             # 추출된 랜드마크와 데이터베이스의 랜드마크들 중 제일 짧은 거리를 찾는 부분
#             descs1 = sorted(descs, key=lambda x: np.linalg.norm([desc] - x[1]))
#             dist = np.linalg.norm([desc] - descs1[0][1], axis=1)
            
#             if dist < 0.45: # 그 거리가 0.45보다 작다면 그 사람으로 판단 
#                 name = descs1[0][0]
#             else:  
#                 try:         # 0.45보다 크다면 모르는 사람으로 판단 -> 모자이크 처리
#                     mosaic_img = cv2.resize(mosaic_img, (w, h), interpolation=cv2.INTER_AREA)
#                     img[y:y+h, x:x+w] = mosaic_img # 인식된 얼굴 영역 모자이크 처리 
#                 except Exception as e:
#                     continue;
        
#             img = Image.fromarray(img)
#             draw = ImageDraw.Draw(img)
#             img = np.array(img)

#             cv2.imshow('result',img)
#             k = cv2.waitKey(10) & 0xff # 'ESC' 키 누르면 종료
#             if k == 27:
#                 break #나중에 삭제
                
#             out.write(img)


#     cap.release()
#     out.release()

#     cap_audio = mp.VideoFileClip("https://summersilicon.s3.ap-northeast-2.amazonaws.com/SchemaName.video/test2.mp4")
#     videoclip = mp.VideoFileClip("last.mp4")
#     result = videoclip.set_audio(cap_audio.audio)


#     result.write_videofile("lastTest.mp4", 
#     codec='libx264', 
#     audio_codec='aac', 
#     temp_audiofile='temp-audio.m4a', 
#     remove_temp=True)