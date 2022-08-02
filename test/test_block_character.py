import unittest
import requests
import json
import config
from requests_toolbelt.multipart.encoder import MultipartEncoder

class BlockCharacterTest(unittest.TestCase):

    def setUp(self):
        self.host = config.path
        self.token = config.token
        
    def test_block_character_origin_read(self):
        response = requests.get(self.host+'/block-characters/origin', headers={"token":self.token})
        data = json.loads(response.text)
        data = data['data']
        print("==================================")
        print("test_block_character_origin_read")
        print(data)
        print("==================================")
        self.assertEqual(200, response.status_code)
        
    def test_block_character_user_upload(self):
        multipart_data = MultipartEncoder(
            fields={
                "file": ('166246.png', open(config.imgPath, 'rb'), 'png')
            }
        )
        response = requests.post(self.host+'/block-characters/user', headers={"Content-Type": multipart_data.content_type, "token":self.token}, data=multipart_data)
        data = json.loads(response.text)
        id = data['id']
        print("==================================")
        print("test_block_character_user_upload")
        print(id)
        print("==================================")
        self.assertEqual(200, response.status_code)
        return id
    
    def test_block_character_user_read(self):
        response = requests.get(self.host+'/block-characters/user', headers={"token":self.token})
        data = json.loads(response.text)
        data = data['data']
        print("==================================")
        print("test_block_character_user_read")
        print(data)
        print("==================================")
        self.assertEqual(200, response.status_code)
    
    def test_block_character_user_delete(self):
        _id = self.test_block_character_user_upload()
        response = requests.delete(self.host+'/block-characters/user/'+_id, headers={"token":self.token})
        data = json.loads(response.text)
        print("==================================")
        print("test_block_character_user_delete")
        print(data['message'])
        print("==================================")
        self.assertEqual(200, response.status_code)
        return id

if __name__ == '__main__':
    unittest.main()