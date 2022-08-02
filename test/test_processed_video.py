import unittest
import requests
import json
import config
from requests_toolbelt.multipart.encoder import MultipartEncoder

class ProcessedVideoTest(unittest.TestCase):

    def setUp(self):
        self.host = config.path
        self.token = config.token
        
    def test_processed_videos_read(self):
        response = requests.get(self.host+'/processed-videos', headers={"token":self.token})
        data = json.loads(response.text)
        data = data['data']
        print("==================================")
        print("test_processed_videos_read")
        print(data)
        print("==================================")
        self.assertEqual(200, response.status_code)
    
    def test_processed_videos_delete(self):
        _id = "62e97e232de81982d49fbcfd"
        response = requests.delete(self.host+'/processed-videos/'+_id, headers={"token":self.token})
        data = json.loads(response.text)
        print("==================================")
        print("test_processed_videos_delete")
        print(data['message'])
        print("==================================")
        self.assertEqual(200, response.status_code)

if __name__ == '__main__':
    unittest.main()