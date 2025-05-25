# # import clickhouse_connect

# # client = clickhouse_connect.get_client(
# #     host='localhost', port=8123, username='svkle', password='Vzvvzv123'
# # )

# # result = client.query('SELECT count() FROM post_events')
# # print(result.result_rows)

# from clickhouse_driver import Client

# client = Client(host='localhost', port=8123, user='svkle', password='Vzvvzv123')
# result = client.execute('SELECT count() FROM post_events')
# print(result)

from clickhouse_driver import Client

# Подключение к ClickHouse (localhost по умолчанию)
client = Client(host='localhost')

# Выполнение запроса
result = client.execute('SELECT * from post_was_commented')
print(result)