import unittest
from main import client
from db.db_posts import get_last_index
from db import db_events as db
from db.db_user import get_user_id
import json

class TestService(unittest.TestCase):
    token = ""
    last_id = 0

    def test_01_check_register(self):
        print("test 1")
        response = client.post("/user_service/register", params={"login": "unit_test_100", "password": "unit_test", "email": "unit_test"})
        print(response.text)
        self.assertTrue(response.status_code == 200)
        self.assertTrue(response.text == "\"User was registered.\"")
    
    def test_02_get_token(self):
        print("test 2")
        response = client.post("/user_service/authentificate", params={"login": "unit_test_12", "password": "unit_test"})
        self.assertTrue(response.status_code == 200)
        TestService.token = response.text[response.text.rfind(" ") + 1:-1]
        text = response.text[:response.text.rfind(" ") + 1]
        self.assertTrue(text == "\"Success, token: ")

    def test_03_update_profile(self):
        print("test 3")
        response = client.post("/user_service/update", params={
            "field": "user_name",
            "value": "unit_test_name",
            "token": TestService.token
        })
        self.assertTrue(response.status_code == 200)
        self.assertTrue(response.text == "\"The field was updated.\"")
        
    # gRPC posts
    def test_04_create_post(self):
        TestService.last_id = get_last_index()
        
        response = client.post("/posts/create_post", params={"token": TestService.token, "title": "title", "is_private":"False", "description":"No", "tags":"test"})
        self.assertTrue(response.status_code == 200)
        resp = json.loads(json.loads(response.text))
        self.assertTrue(resp["message"] == "New post created")
        self.assertTrue(resp["post_id"] == TestService.last_id+1)
    
    def test_05_update_post(self):
        response = client.post("/posts/update_post", params={"token": TestService.token, "post_id":TestService.last_id+1,"title": "newtitle", "is_private":"False", "description":"No", "tags":"test"})
        self.assertTrue(response.status_code == 200)
        resp = json.loads(json.loads(response.text))
        self.assertTrue(resp["message"] == "Post was updated")
        self.assertTrue(resp["post_id"] == TestService.last_id+1)
        
    def test_06_get_post(self):
        response = client.post("/posts/get_post_by_id", params={"token": TestService.token, "post_id":TestService.last_id+1})
        self.assertTrue(response.status_code == 200)
        resp = json.loads(json.loads(response.text))
        self.assertTrue(resp["title"] == "newtitle")
        
    # Kafka
    
    def test_07_user_registered(self):
        response = client.post("/user_service/register", params={"login": "unit_test_101", "password": "unit_test", "email": "unit_test"})
        self.assertTrue(response.status_code == 200)

        self.assertTrue(db.check_response("register", "unit_test_101", "unit_test", "unit_test") == True)
        
    def test_08_post_viewed(self):
        response = client.post("/posts/get_post_by_id", params={"token": TestService.token, "post_id":TestService.last_id+1})
        self.assertTrue(response.status_code == 200)
        
        self.assertTrue(db.check_response("view", get_user_id(TestService.token), TestService.last_id+1) == True)
    
    # gRPC statistics
    
    def test_09_get_likes(self):
        response = client.post("/stat/get_post_likes", params={"token": TestService.token, "post_id":TestService.last_id+1})
        self.assertTrue(response.status_code == 200)
        
        post = db.get_post_info(TestService.last_id+1)
        resp = json.loads(json.loads(response.text))
        self.assertTrue(resp["likes"] == '\"' + str(post["likes"]) + '\"')
        
    def test_10_get_likes_dynamic(self):
        response = client.post("/stat/get_post_likes_dynamic", params={"token": TestService.token, "post_id":TestService.last_id+1})
        self.assertTrue(response.status_code == 200)
        
        post = db.get_post_dynamics(TestService.last_id+1)
        resp = json.loads(json.loads(response.text))
        self.assertTrue(post["likes"] == resp)
        
    def test_11_get_top_like_posts(self):
        response = client.post("/stat/get_top", params={"token": TestService.token, "category": "likes"})
        self.assertTrue(response.status_code == 200)
        
        post = db.get_top(TestService.last_id+1)
        resp = json.loads(json.loads(response.text))
        self.assertTrue(post["likes"] == resp)
        
    # User stories
    
    def test_12_history_1(self):
        # User registers
        response = client.post("/user_service/register", params={"login": "unit_test_102", "password": "unit_test", "email": "unit_test"})
        print(response.text)
        self.assertTrue(response.status_code == 200)
        self.assertTrue(response.text == "\"User was registered.\"")
        
        # User gets his credentials
        response = client.post("/user_service/authentificate", params={"login": "unit_test_102", "password": "unit_test"})
        self.assertTrue(response.status_code == 200)
        TestService.token = response.text[response.text.rfind(" ") + 1:-1]
        text = response.text[:response.text.rfind(" ") + 1]
        self.assertTrue(text == "\"Success, token: ")
        
        # User looks at posts
        response = client.post("/posts/get_posts_list", params={"token": TestService.token})
        self.assertTrue(response.status_code == 200)
        resp = json.loads(json.loads(response.text))
        
        # User creates his own post based on the seen
        TestService.last_id = get_last_index()
        
        response = client.post("/posts/create_post", params={"token": TestService.token, "title": "title", "is_private":"False", "description":"No", "tags":"test"})
        self.assertTrue(response.status_code == 200)
        resp = json.loads(json.loads(response.text))
        self.assertTrue(resp["message"] == "New post created")
        self.assertTrue(resp["post_id"] == TestService.last_id+1)
    
    def test_13_history_2(self):
        # User gets his credentials
        response = client.post("/user_service/authentificate", params={"login": "unit_test_102", "password": "unit_test"})
        self.assertTrue(response.status_code == 200)
        TestService.token = response.text[response.text.rfind(" ") + 1:-1]
        text = response.text[:response.text.rfind(" ") + 1]
        self.assertTrue(text == "\"Success, token: ")
        
        # User looks at posts
        response = client.post("/posts/get_posts_list", params={"token": TestService.token})
        self.assertTrue(response.status_code == 200)
        resp = json.loads(json.loads(response.text))
        
        # User likes a posts
        response = client.post("/posts/like_post", params={"token": TestService.token, "post_id":TestService.last_id+1})
        self.assertTrue(response.status_code == 200)
        
        self.assertTrue(db.check_response("view", get_user_id(TestService.token), TestService.last_id+1) == True)
        self.assertTrue(db.check_response("like", get_user_id(TestService.token), TestService.last_id+1) == True)
        
        # User gets comments
        response = client.post("/stat/get_post_comments", params={"token": TestService.token, "post_id":TestService.last_id+1})
        self.assertTrue(response.status_code == 200)
        
        post = db.get_post_info(TestService.last_id+1)
        resp = json.loads(json.loads(response.text))
        self.assertTrue(resp["comments"] == '\"' + str(post["comments"]) + '\"')
        
        # User comments
        response = client.post("/posts/comment_post", params={"token": TestService.token, "post_id":TestService.last_id+1, "comment": "Good job"})
        self.assertTrue(response.status_code == 200)
        
        self.assertTrue(db.check_response("view", get_user_id(TestService.token), TestService.last_id+1) == True)
        self.assertTrue(db.check_response("comment", get_user_id(TestService.token), TestService.last_id+1, "Good job") == True)
        
    def test_14_history_3(self):
        # User gets his credentials
        response = client.post("/user_service/authentificate", params={"login": "unit_test_102", "password": "unit_test"})
        self.assertTrue(response.status_code == 200)
        TestService.token = response.text[response.text.rfind(" ") + 1:-1]
        text = response.text[:response.text.rfind(" ") + 1]
        self.assertTrue(text == "\"Success, token: ")
        
        # User see posts with most likes
        response = client.post("/stat/get_top", params={"token": TestService.token, "category": "likes"})
        self.assertTrue(response.status_code == 200)
        
        post = db.get_top(TestService.last_id+1)
        resp = json.loads(json.loads(response.text))
        self.assertTrue(post["likes"] == resp)
        
        # User gets the top liked comment
        top_1 = post["likes"][0]
        
        response = client.post("/posts/get_post_by_id", params={"token": TestService.token, "post_id":top_1})
        self.assertTrue(response.status_code == 200)
        resp = json.loads(json.loads(response.text))
        
        # User gets views dynamic
        response = client.post("/stat/get_post_views_dynamic", params={"token": TestService.token, "post_id":top_1})
        self.assertTrue(response.status_code == 200)
        
        post = db.get_post_dynamics(TestService.last_id+1)
        resp = json.loads(json.loads(response.text))
        self.assertTrue(post["views"] == resp)
        
        # User comments
        response = client.post("/posts/comment_post", params={"token": TestService.token, "post_id":top_1, "comment": "Magnificent"})
        self.assertTrue(response.status_code == 200)
        
        self.assertTrue(db.check_response("view", get_user_id(TestService.token), TestService.last_id+1) == True)
        self.assertTrue(db.check_response("comment", get_user_id(TestService.token), TestService.last_id+1, "Magnificent") == True)
    
if __name__ == '__main__':
    unittest.main()