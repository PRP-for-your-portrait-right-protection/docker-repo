import unittest
import requests
import json
import config
from requests_toolbelt.multipart.encoder import MultipartEncoder

class AuthTest(unittest.TestCase):
    global token

    def setUp(self):
        self.host = config.path

    def test_auth(self):
        email = "paurakh011@gmail.com"
        multipart_data = MultipartEncoder(
            fields={
                "email": email,
                "password": "mycoolpassword",
            }
        )
        response = requests.post(self.host+'/auth', headers={"Content-Type": multipart_data.content_type}, data=multipart_data)
        data = json.loads(response.text)
        token = data['token']
        print("==================================")
        print("test_auth")
        print(token)
        print("==================================")
        self.assertEqual(email, data['email'])
        self.assertEqual(200, response.status_code)
        