import unittest
from main import client
from db.db_posts import get_last_index
import json

class TestService(unittest.TestCase):
    def test_posts_service(self):
        response = client.post("/user_service/authentificate", params={"login": "svkle", "password": "test"})
        self.assertTrue(response.status_code == 200)
        token = (response.text)[response.text.rfind(" ")+1:-1]
        print(token)
        
        last_id = get_last_index()
        
        response = client.post("/posts/create_post", params={"token": token, "title": "title", "is_private":"False", "description":"No", "tags":"test"})
        self.assertTrue(response.status_code == 200)
        resp = json.loads(json.loads(response.text))
        self.assertTrue(resp["message"] == "New post created")
        self.assertTrue(resp["post_id"] == last_id+1)
        
        response = client.post("/posts/update_post", params={"token": token, "post_id":last_id+1,"title": "newtitle", "is_private":"False", "description":"No", "tags":"test"})
        self.assertTrue(response.status_code == 200)
        resp = json.loads(json.loads(response.text))
        self.assertTrue(resp["message"] == "Post was updated")
        self.assertTrue(resp["post_id"] == last_id+1)
        
        response = client.post("/posts/get_post_by_id", params={"token": token, "post_id":last_id+1})
        self.assertTrue(response.status_code == 200)
        resp = json.loads(json.loads(response.text))
        self.assertTrue(resp["title"] == "newtitle")
        
        response = client.post("/posts/get_post_by_id", params={"token": token, "post_id":last_id+2})
        print(response.text)
        self.assertTrue(response.status_code == 401)
        self.assertTrue(response.text == "\"Post with id %s was not found.\""%(last_id+2))
        
        response = client.post("/posts/get_posts_list", params={"token": token})
        self.assertTrue(response.status_code == 200)
        resp = json.loads(json.loads(response.text))
        print(resp)
        
if __name__ == '__main__':
    unittest.main()