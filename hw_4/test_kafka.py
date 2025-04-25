import json
from confluent_kafka import Consumer, KafkaException
import unittest
from main import client
from confluent_kafka import Consumer, TopicPartition

conf = {
    'bootstrap.servers': 'localhost:9092',
    'group.id': 'last-message-reader',
    'enable.auto.commit': False,
    'auto.offset.reset': 'earliest'
}

consumer = Consumer(conf)

class TestService(unittest.TestCase):
    def test_check_register(self):
        log = "a"
        response = client.post("/user_service/register", params={"login": log, "password": "test", "email": "test"})
        self.assertTrue(response.status_code == 200)
        self.assertTrue(response.text == "\"User was registered.\"")
        
        topic = 'new_user_was_registered'
        partition = 0
        tp = TopicPartition(topic, partition)
        low, high = consumer.get_watermark_offsets(tp, timeout=5.0)
        if high == 0:
            print("No messages in this partition.")
            self.assertFalse(response.status_code == 400)
        else:
            tp.offset = high - 1
            consumer.assign([tp])
            consumer.seek(tp)
            
            msg = consumer.poll(timeout=5.0)
            if msg and not msg.error():
                print(f"Last register message: {msg.value().decode('utf-8')}")
                message = json.loads(msg.value().decode('utf-8'))
                self.assertTrue(message['user_login'] == log)
                self.assertTrue(message['event_type'] == "new_user_was_registered")
            else:
                print("No message found or error.")
                self.assertFalse(response.status_code == 400)
        
    def test_kafka_work_with_posts(self):
        response = client.get("/user_service/get_new_token_with_login", params={"login": "svkle", "password": "test"})
        self.assertTrue(response.status_code == 200)
        text = (response.text)[:response.text.rfind(" ")+1]
        token = (response.text)[response.text.rfind(" ")+1:-1]
        self.assertTrue(text == "\"New token: ")
        
        # check post viewed
        
        response = client.post("/posts/get_post_by_id", params={"token": token, "post_id":2})
        self.assertTrue(response.status_code == 200)
        
        topic = 'post_was_viewed'
        partition = 0
        tp = TopicPartition(topic, partition)
        low, high = consumer.get_watermark_offsets(tp, timeout=5.0)
        if high == 0:
            print("No messages in this partition.")
            self.assertFalse(response.status_code == 400)
        else:
            tp.offset = high - 1
            consumer.assign([tp])
            consumer.seek(tp)
            
            msg = consumer.poll(timeout=5.0)
            if msg and not msg.error():
                print(f"Last register message: {msg.value().decode('utf-8')}")
                message = json.loads(msg.value().decode('utf-8'))
                self.assertTrue(int(message['user_id']) == 53)
                self.assertTrue(int(message['post_id']) == 2)
                self.assertTrue(message['event_type'] == "post_was_viewed")
            else:
                print("No message found or error.")
                self.assertFalse(response.status_code == 400)
        
        # check post viewed and commented
        
        response = client.post("/posts/comment_post", params={"token": token, "post_id":2, "comment": "Wow, great job!"})
        self.assertTrue(response.status_code == 200)
        
        topic = 'post_was_viewed'
        partition = 0
        tp = TopicPartition(topic, partition)
        low, high = consumer.get_watermark_offsets(tp, timeout=5.0)
        if high == 0:
            print("No messages in this partition.")
            self.assertFalse(response.status_code == 400)
        else:
            tp.offset = high - 1
            consumer.assign([tp])
            consumer.seek(tp)
            
            msg = consumer.poll(timeout=5.0)
            if msg and not msg.error():
                print(f"Last register message: {msg.value().decode('utf-8')}")
                message = json.loads(msg.value().decode('utf-8'))
                self.assertTrue(int(message['user_id']) == 53)
                self.assertTrue(int(message['post_id']) == 2)
                self.assertTrue(message['event_type'] == "post_was_viewed")
            else:
                print("No message found or error.")
                self.assertFalse(response.status_code == 400)
                
        topic = 'post_was_commented'
        partition = 0
        tp = TopicPartition(topic, partition)
        low, high = consumer.get_watermark_offsets(tp, timeout=5.0)
        if high == 0:
            print("No messages in this partition.")
            self.assertFalse(response.status_code == 400)
        else:
            tp.offset = high - 1
            consumer.assign([tp])
            consumer.seek(tp)
            
            msg = consumer.poll(timeout=5.0)
            if msg and not msg.error():
                print(f"Last register message: {msg.value().decode('utf-8')}")
                message = json.loads(msg.value().decode('utf-8'))
                self.assertTrue(int(message['user_id']) == 53)
                self.assertTrue(int(message['post_id']) == 2)
                self.assertTrue(message['event_type'] == "post_was_commented")
                self.assertTrue(message['comment'] == "Wow, great job!")
            else:
                print("No message found or error.")
                self.assertFalse(response.status_code == 400)
                
        # check post viewed and liked
        
        response = client.post("/posts/comment_post", params={"token": token, "post_id":2, "comment": "Wow, great job!"})
        self.assertTrue(response.status_code == 200)
        
        topic = 'post_was_viewed'
        partition = 0
        tp = TopicPartition(topic, partition)
        low, high = consumer.get_watermark_offsets(tp, timeout=5.0)
        if high == 0:
            print("No messages in this partition.")
            self.assertFalse(response.status_code == 400)
        else:
            tp.offset = high - 1
            consumer.assign([tp])
            consumer.seek(tp)
            
            msg = consumer.poll(timeout=5.0)
            if msg and not msg.error():
                print(f"Last register message: {msg.value().decode('utf-8')}")
                message = json.loads(msg.value().decode('utf-8'))
                self.assertTrue(int(message['user_id']) == 53)
                self.assertTrue(int(message['post_id']) == 2)
                self.assertTrue(message['event_type'] == "post_was_viewed")
            else:
                print("No message found or error.")
                self.assertFalse(response.status_code == 400)
                
        topic = 'post_was_liked'
        partition = 0
        tp = TopicPartition(topic, partition)
        low, high = consumer.get_watermark_offsets(tp, timeout=5.0)
        if high == 0:
            print("No messages in this partition.")
            self.assertFalse(response.status_code == 400)
        else:
            tp.offset = high - 1
            consumer.assign([tp])
            consumer.seek(tp)
            
            msg = consumer.poll(timeout=5.0)
            if msg and not msg.error():
                print(f"Last register message: {msg.value().decode('utf-8')}")
                message = json.loads(msg.value().decode('utf-8'))
                self.assertTrue(int(message['user_id']) == 53)
                self.assertTrue(int(message['post_id']) == 2)
                self.assertTrue(message['event_type'] == "post_was_liked")
            else:
                print("No message found or error.")
                self.assertFalse(response.status_code == 400)

if __name__ == '__main__':
    unittest.main()