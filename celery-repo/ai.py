'''
from google.colab.patches import cv2_imshow
 
import numpy as np
import cv2
import pafy
import moviepy.editor as mp #소리 추출
#--------
# 라이브러리
import dlib
import matplotlib.pyplot as plt
from PIL import ImageFont, ImageDraw, Image
import tensorflow.keras 
from tensorflow.keras import backend as K
import time




detector = dlib.get_frontal_face_detector()
sp = dlib.shape_predictor('/content/drive/MyDrive/shape_predictor_68_face_landmarks.dat')
facerec = dlib.face_recognition_model_v1('/content/drive/MyDrive/dlib_face_recognition_resnet_model_v1.dat')

 

def find_faces(img):
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
    face_descriptors = []
    for shape in shapes:
        face_descriptor = facerec.compute_face_descriptor(img, shape)
        face_descriptors.append(np.array(face_descriptor))

    return np.array(face_descriptors)


img_paths = {  ##여기서 특정인물들에 대한 사진을 입력합니다. 앞에 "특정인물1" 이런거는 불필요한 변수이긴해요. 향후 입력값으로 받아서 for문돌리면서 넣는식으로 진행해야합니다.
     '특정인물1': "/content/drive/MyDrive/user1.png",
     '특정인물2': "/content/drive/MyDrive/user2.png",
     '특정인물3': "/content/drive/MyDrive/user3.png"
  
}

descs = []
for name, img_path in img_paths.items(): 
    img = cv2.imread(img_path)
    _, img_shapes, _ = find_faces(img)
    descs.append([name, encode_faces(img, img_shapes)[0]])
    
np.save("/content/drive/MyDrive/descs.npy", descs)




#url = 'https://www.youtube.com/watch?v=S_0ikqqccJs' #url 링크 (추후 사용자로부터 입력받은 영상파일 && 옵션에 따라 실시간 영상처리)
#video = pafy.new(url)

#best = video.getbest(preftype="mp4")

cap = cv2.VideoCapture("/content/drive/MyDrive/test.mp4") #직접 영상 사용  ##입력받은 영상의 url?을 넣습니다. 이부분도 props로 받아서 넣어주어야해요.
##cap = cv2.VideoCapture(0) # 노트북 웹캠을 카메라로 사용 

xml = "/content/drive/MyDrive/haarcascade_frontalface_default.xml" #얼굴인식과 관련된 xml , 정확도가 떨어져서 이 부분만 따로 학습시키거나 해야..?

mosaic_img = cv2.imread('/content/drive/MyDrive/user1.png') #캐릭터 이미지로 변환 시 사용 ##변환시 사용하는 이미지입니다.

res=(int(cap.get(3)),int(cap.get(4))) #resulotion
fourcc = cv2.VideoWriter_fourcc(*'DIVX') #codec
out = cv2.VideoWriter('/content/drive/MyDrive/last.mp4', fourcc, 30.0, res) #저장할 영상의 파일 명  ##어떤파일명으로 저장할 지 정하지만 이 파일명은 최종이 아닙니다. 여기서 나온 결과물과 소리를 합성해야해요

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
            mosaic_img = cv2.resize(img[y:y+h, x:x+w], dsize=(0, 0), fx=0.04, fy=0.04) # 축소
            mosaic_img = cv2.resize(mosaic_img, (w, h), interpolation=cv2.INTER_AREA)  # 확대
            img[y:y+h, x:x+w] = mosaic_img # 인식된 얼굴 영역 모자이크 처리 
          except Exception as e:
            continue;

        cv2.rectangle(img, (x, y), (x+w, y+h), (0,255,0), 2) # 얼굴 영역 박스 
       
       
    img = Image.fromarray(img)
    draw = ImageDraw.Draw(img)
    img = np.array(img)
        
    out.write(img)
  

cap.release()
out.release()

cap_audio = mp.VideoFileClip("/content/drive/MyDrive/test.mp4")
videoclip = mp.VideoFileClip("/content/drive/MyDrive/last.mp4")
result = videoclip.set_audio(cap_audio.audio)


result.write_videofile("/content/drive/MyDrive/lastTest.mp4", 
  codec='libx264', 
  audio_codec='aac', 
  temp_audiofile='temp-audio.m4a', 
  remove_temp=True
)
# ds
'''
def return_x(x):
    a = x
    return a