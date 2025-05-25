import json
from datetime import datetime
from kafka import KafkaConsumer
from clickhouse_driver import Client

KAFKA_TOPICS = [
    'new_user_was_registered',
    'post_was_commented',
    'post_was_liked',
    'post_was_viewed'
]
KAFKA_BOOTSTRAP_SERVERS = ['localhost:9092']

ch_client = Client(host='localhost')

consumer = KafkaConsumer(
    *KAFKA_TOPICS,
    bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='clickhouse_group_5',
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

running = True

print("Listening to Kafka topics:", KAFKA_TOPICS)

for message in consumer:
    if not running:
        break

    topic = message.topic
    event = message.value

    print(f"Topic: {topic} | Message: {event}")

    try:
        ts = datetime.fromisoformat(event["timestamp"].replace("Z", "+00:00"))

        if topic == 'new_user_was_registered':
            ch_client.execute(
                "INSERT INTO new_user_was_registered (event_type, timestamp, user_id, user_login, user_email) VALUES",
                [(event['event_type'], ts, event['user_id'], event['user_login'], event['user_email'])]
            )

        elif topic == 'post_was_commented':
            ch_client.execute(
                "INSERT INTO post_was_commented (event_type, timestamp, post_id, user_id, comment) VALUES",
                [(event['event_type'], ts, event['post_id'], event['user_id'], event['comment'])]
            )

        elif topic == 'post_was_liked':
            ch_client.execute(
                "INSERT INTO post_was_liked (event_type, timestamp, post_id, user_id) VALUES",
                [(event['event_type'], ts, event['post_id'], event['user_id'])]
            )

        elif topic == 'post_was_viewed':
            ch_client.execute(
                "INSERT INTO post_was_viewed (event_type, timestamp, post_id, user_id) VALUES",
                [(event['event_type'], ts, event['post_id'], event['user_id'])]
            )

        print(f"Inserted into ClickHouse table for topic: {topic}")

    except Exception as e:
        print(f"Error processing message from topic {topic}: {e}")