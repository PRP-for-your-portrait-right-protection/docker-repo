import os
import cv2
from module.face_module import find_faces, encode_faces

def download_file(img_paths, user, taskId):
    local_img_paths = []
    for img_path in img_paths:
        name = img_path.split('/')[4]
        os.system("curl " + img_path + f' > {user}/{taskId}/{name}')
        img_paths[img_paths.index(img_path)] = f' > {user}/{taskId}/{name}'
        local_img_paths.append(f'{user}/{taskId}/{name}')
    return local_img_paths

def read_img(local_img_paths):
    name = ""
    descs = []
    for img_path in local_img_paths: 
        img = cv2.imread(img_path)
        _, img_shapes, _ = find_faces(img)
        descs.append([name, encode_faces(img, img_shapes)[0]])
    return descs

def download_character_img(user, taskId, blockCharacterUrl):
    name = blockCharacterUrl.split('/')[4]
    os.system("curl " + blockCharacterUrl + f' > {user}/{taskId}/{name}')
    return f'{user}/{taskId}/{name}'
