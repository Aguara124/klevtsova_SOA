import unittest
from main import client

class TestService(unittest.TestCase):
    def test_check_register(self):
        response = client.post("/user_service/register", params={"login": "unit_test_25", "password": "unit_test", "email": "unit_test"})
        print(response.text)
        self.assertTrue(response.status_code == 200)
        self.assertTrue(response.text == "\"User was registered.\"")
        
    def test_check_if_user_already_exists(self):
        response = client.post("/user_service/register", params={"login": "unit_test_12", "password": "unit_test", "email": "unit_test"})
        self.assertTrue(response.status_code == 400)
        self.assertTrue(response.text == "\"Current login already exists.\"")
        
    def test_authentificate_get_token_update_and_get_info(self):
        # test authentificate
        response = client.post("/user_service/authentificate", params={"login": "unit_test_12", "password": "unit_test"})
        self.assertTrue(response.status_code == 200)
        token = (response.text)[response.text.rfind(" ")+1:-1]
        text = (response.text)[:response.text.rfind(" ")+1]
        self.assertTrue(text == "\"Success, token: ")
        # test getting new token by old token
        response = client.get("/user_service/get_new_token", params={"token": token})
        self.assertTrue(response.status_code == 200)
        text = (response.text)[:response.text.rfind(" ")+1]
        self.assertTrue(text == "\"New token: ")
        # test getting new token by credentials
        response = client.get("/user_service/get_new_token_with_login", params={"login": "unit_test_12", "password": "unit_test"})
        self.assertTrue(response.status_code == 200)
        text = (response.text)[:response.text.rfind(" ")+1]
        token = (response.text)[response.text.rfind(" ")+1:-1]
        self.assertTrue(text == "\"New token: ")
        # test getting information by token
        response = client.get("/user_service/get_info", params={"token": token})
        self.assertTrue(response.status_code == 200)
        arr = (response.text).split(',')
        arr.pop(8)
        corrected = ""
        corrected = ','.join(arr)
        print(corrected)
        self.assertTrue(corrected == "[23,null,null,null,\"unit_test\",\"unit_test_12\",\"dW5pdF90ZXN0\",\"2025-03-04 18:58:15.410657\",\"%s\"]"%(str(token)))
        # test updating
        response = client.post("/user_service/update", params={"field": "user_name", "value": "unit_test_name", "token":token})
        self.assertTrue(response.status_code == 200)
        self.assertTrue(response.text == "\"The field was updated.\"")
        # check that was updated
        response = client.get("/user_service/get_info", params={"token": token})
        self.assertTrue(response.status_code == 200)
        arr = (response.text).split(',')
        print(response.text)
        arr.pop(8)
        corrected = ""
        corrected = ','.join(arr)
        print(corrected)
        self.assertTrue(corrected == "[23,\"unit_test_name\",null,null,\"unit_test\",\"unit_test_12\",\"dW5pdF90ZXN0\",\"2025-03-04 18:58:15.410657\",\"%s\"]"%(str(token)))
        
    def test_expired_token(self):
        response = client.get("/user_service/get_info", params={"token": "0837ba16-4de3-48f5-97dc-952ab9b0e59e"})
        self.assertTrue(response.status_code == 401)
        self.assertTrue(response.text == "\"The token is expired. Create a new one using /get_new_token_login.\"")
        
if __name__ == '__main__':
    unittest.main()