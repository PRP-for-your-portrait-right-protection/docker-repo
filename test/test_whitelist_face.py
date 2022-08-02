import unittest
import requests
import json
import config
from requests_toolbelt.multipart.encoder import MultipartEncoder

class WhitelistFaceTest(unittest.TestCase):

    def setUp(self):
        self.host = config.path
        self.token = config.token
        self._id = self.test_whitelist_faces_upload()
        
    def test_whitelist_faces_upload(self):
        multipart_data = MultipartEncoder(
            fields={
                "name": "james",
            }
        )
        response = requests.post(self.host+'/whitelist-faces', headers={"Content-Type": multipart_data.content_type, "token":self.token}, data=multipart_data)
        data = json.loads(response.text)
        id = data['id']
        print("==================================")
        print("test_whitelist_faces_upload")
        print(id)
        print("==================================")
        self.assertEqual(200, response.status_code)
        return id
    
    def test_whitelist_faces_images_read(self):
        response = requests.get(self.host+'/whitelist-faces/images', headers={"token":self.token})
        data = json.loads(response.text)
        data = data['data']
        print("==================================")
        print("test_whitelist_faces_images_read")
        print(data)
        print("==================================")
        self.assertEqual(200, response.status_code)
        return id
    
    def test_whitelist_faces_name_update(self):
        multipart_data = MultipartEncoder(
            fields={
                "face_name_after": "Tom",
            }
        )
        response = requests.patch(self.host+'/whitelist-faces/'+self._id, headers={"Content-Type": multipart_data.content_type, "token":self.token}, data=multipart_data)
        data = json.loads(response.text)
        print("==================================")
        print("test_whitelist_faces_name_update")
        print(data['message'])
        print("==================================")
        self.assertEqual(200, response.status_code)
    
    def test_whitelist_faces_delete(self):
        response = requests.delete(self.host+'/whitelist-faces/'+self._id, headers={"token":self.token})
        data = json.loads(response.text)
        print("==================================")
        print("test_whitelist_faces_delete")
        print(data['message'])
        print("==================================")
        self.assertEqual(200, response.status_code)
        
    def test_whitelist_faces_images_upload(self):
        multipart_data = MultipartEncoder(
            fields={
                "file": ('166246.png', open(config.imgPath, 'rb'), 'png')
            }
        )
        response = requests.post(self.host+'/whitelist-faces/' + self._id + '/images', headers={"Content-Type": multipart_data.content_type, "token":self.token}, data=multipart_data)
        data = json.loads(response.text)
        id = data['id']
        print("==================================")
        print("test_whitelist_faces_images_upload")
        print(id)
        print("==================================")
        self.assertEqual(200, response.status_code)
        return id
    
    def test_whitelist_faces_images_delete(self):
        _id = self.test_whitelist_faces_images_upload()
        response = requests.delete(self.host+'/whitelist-faces/' + self._id + '/images/' + _id, headers={"token":self.token})
        data = json.loads(response.text)
        print("==================================")
        print("test_whitelist_faces_images_delete")
        print(data['message'])
        print("==================================")
        self.assertEqual(200, response.status_code)
        return id

if __name__ == '__main__':
    unittest.main()