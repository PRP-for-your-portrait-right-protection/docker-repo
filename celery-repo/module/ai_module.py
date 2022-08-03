import numpy as np
import cv2
import moviepy.editor as mp #소리 추출
from PIL import ImageFont, ImageDraw, Image
from datetime import datetime
from module.face_module import find_faces, encode_faces
from bucket.m_connection import s3_upload
from module.file_module import download_file, read_img, download_character_img
import os
import shutil

def mosaic(taskId, logger, whitelistFaceImgList, videoUrl, user):
    logger.info('Got Request - Starting work ')
    logger.info(whitelistFaceImgList)
    logger.info(videoUrl)
    logger.info(user)

    # 유저 이름으로 폴더 생성 (폴더가 존재하지 않는 경우에 생성)
    if not os.path.isdir(user):
        os.mkdir(user)

    if not os.path.isdir(f'{user}/{taskId}'):
        os.mkdir(f'{user}/{taskId}')

    img_paths = whitelistFaceImgList

    name = ""

    local_img_paths = download_file(img_paths, user, taskId)
    descs = read_img(local_img_paths)
        
    np.save(f'{user}/{taskId}/descs.npy', descs)

    os.system("curl " + videoUrl + f' > {user}/{taskId}/before.mp4')
    cap = cv2.VideoCapture(f'{user}/{taskId}/before.mp4') #직접 영상 사용  ##입력받은 영상의 url?을 넣습니다. 이부분도 props로 받아서 넣어주어야해요.

    xml = "/celery/module/ai_requirements/haarcascade_frontalface_default.xml" #얼굴인식과 관련된 xml , 정확도가 떨어져서 이 부분만 따로 학습시키거나 해야..?

    res=(int(cap.get(3)),int(cap.get(4))) #resulotion

    fourcc = cv2.VideoWriter_fourcc('m','p','4','v')
    out = cv2.VideoWriter(f'{user}/{taskId}/last.mp4', fourcc, 30.0, res) #저장할 영상의 파일 명  ##어떤파일명으로 저장할 지 정하지만 이 파일명은 최종이 아닙니다. 여기서 나온 결과물과 소리를 합성해야해요

    while True:
        ret, img = cap.read() 

        logger.info(datetime.now())

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

        img = Image.fromarray(img)
        draw = ImageDraw.Draw(img)
        img = np.array(img)

        out.write(img)

    cap.release()
    out.release()

    cap_audio = mp.VideoFileClip(f'{user}/{taskId}/before.mp4')
    videoclip = mp.VideoFileClip(f'{user}/{taskId}/last.mp4')
    result = videoclip.set_audio(cap_audio.audio)

    temp = f'{user}_after_{datetime.now().strftime("%Y-%m-%d")}.mp4'

    result.write_videofile(f'{user}/{taskId}/{temp}', 
    codec='libx264', 
    audio_codec='aac', 
    temp_audiofile='temp-audio.m4a', 
    remove_temp=True)

    location = s3_upload(user, taskId, temp)

    # 만들었던 폴더 삭제
    if os.path.exists(f'{user}/{taskId}'):
        shutil.rmtree(f'{user}/{taskId}')

    logger.info('Work Finished ')

    if location != False:
        return location
    else:
        return False

def character(taskId, logger, whitelistFaceImgList, blockCharacterImgUrl, videoUrl, user):
    logger.info('Got Request - Starting work ')
    logger.info(whitelistFaceImgList)
    logger.info(videoUrl)
    logger.info(user)
    
    # 유저 이름으로 폴더 생성 (폴더가 존재하지 않는 경우에 생성)
    if not os.path.isdir(user):
        os.mkdir(user)

    if not os.path.isdir(f'{user}/{taskId}'):
        os.mkdir(f'{user}/{taskId}')

    img_paths = whitelistFaceImgList   

    name = ""

    local_img_paths = download_file(img_paths, user, taskId)
    descs = read_img(local_img_paths)
        
    np.save(f'{user}/{taskId}/descs.npy', descs)

    os.system("curl " + videoUrl + f' > {user}/{taskId}/before.mp4')
    cap = cv2.VideoCapture(f'{user}/{taskId}/before.mp4') #직접 영상 사용  ##입력받은 영상의 url?을 넣습니다. 이부분도 props로 받아서 넣어주어야해요.

    xml = "/celery/module/ai_requirements/haarcascade_frontalface_default.xml" #얼굴인식과 관련된 xml , 정확도가 떨어져서 이 부분만 따로 학습시키거나 해야..?

    blockCharacterImgUrl = download_character_img(user, taskId, blockCharacterImgUrl)
    mosaic_img = cv2.imread(blockCharacterImgUrl) #캐릭터 이미지로 변환 시 사용 ##변환시 사용하는 이미지입니다.

    res=(int(cap.get(3)),int(cap.get(4))) #resulotion

    # fourcc = cv2.VideoWriter_fourcc(*'DIVX') #codec
    # out = cv2.VideoWriter('last.mp4', fourcc, 30.0, res) #저장할 영상의 파일 명  ##어떤파일명으로 저장할 지 정하지만 이 파일명은 최종이 아닙니다. 여기서 나온 결과물과 소리를 합성해야해요
    fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
    out = cv2.VideoWriter(f'{user}/{taskId}/last.mp4', fourcc, 30.0, res) #저장할 영상의 파일 명  ##어떤파일명으로 저장할 지 정하지만 이 파일명은 최종이 아닙니다. 여기서 나온 결과물과 소리를 합성해야해요

    while True:
        ret, img = cap.read()

        logger.info(datetime.now())

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
                    mosaic_img = cv2.resize(mosaic_img, (w, h), interpolation=cv2.INTER_AREA)
                    img[y:y+h, x:x+w] = mosaic_img 
                except Exception as e:
                    continue;
        
        img = Image.fromarray(img)
        draw = ImageDraw.Draw(img)
        img = np.array(img)
            
        out.write(img)

    cap.release()
    out.release()

    cap_audio = mp.VideoFileClip(f'{user}/{taskId}/before.mp4')
    videoclip = mp.VideoFileClip(f'{user}/{taskId}/last.mp4')
    result = videoclip.set_audio(cap_audio.audio)

    temp = f'{user}_after_{datetime.now().strftime("%Y-%m-%d")}.mp4'

    result.write_videofile(f'{user}/{taskId}/{temp}', 
    codec='libx264', 
    audio_codec='aac', 
    temp_audiofile='temp-audio.m4a', 
    remove_temp=True)

    location = s3_upload(user, taskId, temp)

    # 만들었던 폴더 삭제
    if os.path.exists(f'{user}/{taskId}'):
        shutil.rmtree(f'{user}/{taskId}')

    logger.info('Work Finished ')

    if location != False:
        return location
    else:
        return False