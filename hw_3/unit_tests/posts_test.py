import unittest
from main import client

class TestService(unittest.TestCase):
    def test_creation(self):
        response = client.post("/posts/create_post", params={"token": "unit_test_25", "password": "unit_test", "email": "unit_test"})
        # to be continued
        
if __name__ == '__main__':
    unittest.main()