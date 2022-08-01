import numpy as np
# import cv2
import moviepy.editor as mp #소리 추출
import dlib
# import tensorflow.keras 
# from tensorflow.keras import backend as K
# import matplotlib.pyplot as plt 
# from PIL import ImageFont, ImageDraw, Image
# import time

def find_faces(img):
    detector = dlib.get_frontal_face_detector()
    sp = dlib.shape_predictor('/celery/module/ai_requirements/shape_predictor_68_face_landmarks.dat')
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
    facerec = dlib.face_recognition_model_v1('/celery/module/ai_requirements/dlib_face_recognition_resnet_model_v1.dat')
    face_descriptors = []
    for shape in shapes:
        face_descriptor = facerec.compute_face_descriptor(img, shape)
        face_descriptors.append(np.array(face_descriptor))

    return np.array(face_descriptors)