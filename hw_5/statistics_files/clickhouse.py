from technical_files.protos.generated import stats_pb2_grpc, stats_pb2

from clickhouse_driver import Client

client = Client(host='localhost')

def GetPostStats(self, request, context):
    post_id = request.post_id
    views = client.execute("SELECT count() FROM post_was_viewed WHERE post_id=%s", (post_id,))[0][0]
    likes = client.execute("SELECT count() FROM post_was_liked WHERE post_id=%s", (post_id,))[0][0]
    comments = client.execute("SELECT count() FROM post_was_commented WHERE post_id=%s", (post_id,))[0][0]
    return stats_pb2.PostStatsResponse(views=views, likes=likes, comments=comments)