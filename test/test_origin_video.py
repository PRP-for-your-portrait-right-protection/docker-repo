import unittest
import requests
import json
import config
from requests_toolbelt.multipart.encoder import MultipartEncoder

class OriginVideoTest(unittest.TestCase):

    def setUp(self):
        self.host = config.path
        self.token = config.token
        
    def test_origin_video_upload(self):
        multipart_data = MultipartEncoder(
            fields={
                "file": ('1.mov', open(config.videoPath, 'rb'), 'mov')
            }
        )
        response = requests.post(self.host+'/origin-videos', headers={"Content-Type": multipart_data.content_type, "token":self.token}, data=multipart_data)
        data = json.loads(response.text)
        id = data['id']
        print("==================================")
        print("test_origin_video_upload")
        print(id)
        print("==================================")
        self.assertEqual(200, response.status_code)
        return id
    
if __name__ == '__main__':
    unittest.main()