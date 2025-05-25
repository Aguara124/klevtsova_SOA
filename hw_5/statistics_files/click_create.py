from clickhouse_driver import Client

client = Client(host='localhost')

client.execute("""
CREATE TABLE IF NOT EXISTS new_user_was_registered (
    event_type String,
    timestamp DateTime,
    user_id UInt64,
    user_login String,
    user_email String
) ENGINE = MergeTree
ORDER BY (user_id, timestamp)
""")

client.execute("""
CREATE TABLE IF NOT EXISTS post_was_commented (
    event_type String,
    timestamp DateTime,
    post_id String,
    user_id UInt64,
    comment String
) ENGINE = MergeTree
ORDER BY (post_id, timestamp)
""")

client.execute("""
CREATE TABLE IF NOT EXISTS post_was_liked (
    event_type String,
    timestamp DateTime,
    post_id String,
    user_id UInt64
) ENGINE = MergeTree
ORDER BY (post_id, timestamp)
""")

client.execute("""
CREATE TABLE IF NOT EXISTS post_was_viewed (
    event_type String,
    timestamp DateTime,
    post_id String,
    user_id UInt64
) ENGINE = MergeTree
ORDER BY (post_id, timestamp)
""")
