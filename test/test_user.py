import unittest
import requests
import json
import config
from requests_toolbelt.multipart.encoder import MultipartEncoder

class UserTest(unittest.TestCase):

    def setUp(self):
        self.host = config.path

    def test_users(self):
        email = "paurakh011@gmail.com"
        multipart_data = MultipartEncoder(
            fields={
                "email": email,
                "password": "mycoolpassword",
                "name": "james",
                "phone":"010-1234-5678"
            }
        )
        response = requests.post(self.host+'/users', headers={"Content-Type": multipart_data.content_type}, data=multipart_data)
        data = json.loads(response.text)
        print(data['id'])
        print(response.status_code)
        self.assertEqual(email, data['id'])
        self.assertEqual(201, response.status_code)
        
    def test_users_email(self):
        multipart_data = MultipartEncoder(
            fields={
                "name": "james",
                "phone":"010-1234-5678"
            }
        )
        response = requests.post(self.host+'/users/email', headers={"Content-Type": multipart_data.content_type}, data=multipart_data)
        data = json.loads(response.text)
        print(data['email'])
        print(response.status_code)
        self.assertEqual(200, response.status_code)
        
    def test_users_email_validation(self):
        multipart_data = MultipartEncoder(
            fields={
                "email": "paurakh011087@gmail.com",
            }
        )
        response = requests.post(self.host+'/users/email/validation', headers={"Content-Type": multipart_data.content_type}, data=multipart_data)
        data = json.loads(response.text)
        print(data['message'])
        print(response.status_code)
        self.assertEqual(200, response.status_code)
        
    def test_users_password(self):
        multipart_data = MultipartEncoder(
            fields={
                "email": "paurakh011@gmail.com",
                "password": "mycoolpassword",
                "phone":"010-1234-5678"
            }
        )
        response = requests.patch(self.host+'/users/password', headers={"Content-Type": multipart_data.content_type}, data=multipart_data)
        data = json.loads(response.text)
        print(data['message'])
        print(response.status_code)
        self.assertEqual(200, response.status_code)
        
    def test_users_password_validation(self):
        multipart_data = MultipartEncoder(
            fields={
                "email": "paurakh011@gmail.com",
                "phone":"010-1234-5678"
            }
        )
        response = requests.post(self.host+'/users/password/validation', headers={"Content-Type": multipart_data.content_type}, data=multipart_data)
        data = json.loads(response.text)
        print(data['message'])
        print(response.status_code)
        self.assertEqual(200, response.status_code)

if __name__ == '__main__':
    unittest.main()