import json
import os
from datetime import datetime
from typing import Dict, Any, Optional
from confluent_kafka import Producer


class KafkaProducer:
    def __init__(self):
        self.producer = Producer({
            'bootstrap.servers': 'localhost:9092',
            'client.id': 'social_network_service_producer'
        })
        
        # Define topics
        self.USER_REGISTERED_TOPIC = "new_user_was_registered"
        self.POST_WAS_VIEWED_TOPIC = "post_was_viewed"
        self.POST_WAS_LIKED_TOPIC = "post_was_liked" # can not be called without calling POST_WAS_VIEWED
        self.POST_WAS_COMMENTED_TOPIC = "post_was_commented" # can not be called without calling POST_WAS_VIEWED
    
    def _delivery_report(self, err, msg):
        """Called once for each message produced to indicate delivery result."""
        if err is not None:
            print(f'Message delivery failed: {err}')
        else:
            print(f'Message delivered to {msg.topic()} [{msg.partition()}]')
    
    def _serialize_datetime(self, obj):
        """JSON serializer for datetime objects."""
        if isinstance(obj, datetime):
            return obj.isoformat()
        raise TypeError(f"Type {type(obj)} not serializable")
    
    def send_event(self, topic: str, data: Dict[str, Any], key: Optional[str] = None):
        """Send an event to the specified Kafka topic."""
        payload = json.dumps(data, default=self._serialize_datetime).encode('utf-8')
        self.producer.produce(
            topic=topic,
            key=key.encode('utf-8') if key else None,
            value=payload,
            callback=self._delivery_report
        )
        # Flush to ensure message is sent immediately
        self.producer.flush()
    
    def send_user_registered_event(self, user_id:int, user_login:str, user_email:str):
        """Send event when a new user is registered."""
        self.send_event(
            topic=self.USER_REGISTERED_TOPIC,
            data={
                "event_type": "new_user_was_registered",
                "timestamp": datetime.now(),
                "user_id": user_id,
                "user_login": user_login,
                "user_email": user_email
            },
            key=str(user_id)
        )
    
    def send_post_viewed_event(self, post_id: int, user_id: int):
        """Send event when a post is viewed."""
        self.send_event(
            topic=self.POST_WAS_VIEWED_TOPIC,
            data={
                "event_type": "post_was_viewed",
                "timestamp": datetime.now(),
                "post_id": post_id,
                "user_id": user_id
            },
            key=str(post_id)
        )
    
    def send_post_liked_event(self, post_id: int, user_id: int):
        """Send event when a post is liked."""
        self.send_event(
            topic=self.POST_WAS_LIKED_TOPIC,
            data={
                "event_type": "post_was_liked",
                "timestamp": datetime.now(),
                "post_id": post_id,
                "user_id": user_id
            },
            key=str(post_id)
        )
        
    def send_post_commented_event(self, post_id: int, user_id: int, comment:str):
        """Send event when a post is commented."""
        self.send_event(
            topic=self.POST_WAS_COMMENTED_TOPIC,
            data={
                "event_type": "post_was_commented",
                "timestamp": datetime.now(),
                "post_id": post_id,
                "user_id": user_id,
                "comment": comment
            },
            key=str(post_id)
        ) 