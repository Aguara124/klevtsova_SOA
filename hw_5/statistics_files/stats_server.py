from concurrent import futures
import grpc
from technical_files.protos.generated import stats_pb2_grpc, stats_pb2
from datetime import datetime, timedelta, timezone
from clickhouse_driver import Client

class StatisticsService(stats_pb2_grpc.StatisticsServiceServicer):
    def __init__(self):
        self.ch_client = Client(host='localhost')

    def GetPostStats(self, request, context):
        post_id = request.post_id
        query = """
            SELECT 
                sumIf(1, event_type = 'post_was_viewed') AS views,
                sumIf(1, event_type = 'post_was_liked') AS likes,
                sumIf(1, event_type = 'post_was_commented') AS comments
            FROM events
            WHERE post_id = %(post_id)s
        """
        result = self.ch_client.execute(query, {'post_id': post_id})
        if result:
            views, likes, comments = result[0]
        else:
            views = likes = comments = 0

        return stats_pb2.PostStatsResponse(
            views=views or 0,
            likes=likes or 0,
            comments=comments or 0
        )

    def _get_post_dynamics(self, post_id, event_type):
        query = """
            SELECT toDate(timestamp) AS day, count() AS cnt
            FROM events
            WHERE post_id = %(post_id)s AND event_type = %(event_type)s
                AND timestamp >= today() - 7
            GROUP BY day
            ORDER BY day DESC
        """
        rows = self.ch_client.execute(query, {'post_id': post_id, 'event_type': event_type})
        
        today = datetime.now(timezone.utc).date()
        counts_by_day = {row[0]: row[1] for row in rows}
        entries = []
        for i in range(7):
            day = today - timedelta(days=i)
            count = counts_by_day.get(day, 0)
            entries.append(stats_pb2.DynamicsEntry(date=day.isoformat(), count=count))
        return entries

    def GetPostViewsDynamics(self, request, context):
        entries = self._get_post_dynamics(request.post_id, 'post_was_viewed')
        return stats_pb2.DynamicsResponse(entries=entries)

    def GetPostLikesDynamics(self, request, context):
        entries = self._get_post_dynamics(request.post_id, 'post_was_liked')
        return stats_pb2.DynamicsResponse(entries=entries)

    def GetPostCommentsDynamics(self, request, context):
        entries = self._get_post_dynamics(request.post_id, 'post_was_commented')
        return stats_pb2.DynamicsResponse(entries=entries)

    def GetTopPosts(self, request, context):
        metric = request.metric
        event_map = {
            'views': 'post_was_viewed',
            'likes': 'post_was_liked',
            'comments': 'post_was_commented'
        }
        event_type = event_map.get(metric)
        if not event_type:
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details(f'Unknown metric: {metric}')
            return stats_pb2.TopPostsResponse(posts=[])

        query = """
            SELECT post_id, count() AS cnt
            FROM events
            WHERE event_type = %(event_type)s
            GROUP BY post_id
            ORDER BY cnt DESC
            LIMIT 10
        """
        rows = self.ch_client.execute(query, {'event_type': event_type})
        posts = [stats_pb2.PostCount(post_id=str(row[0]), count=row[1]) for row in rows]
        return stats_pb2.TopPostsResponse(posts=posts)

    def GetTopUsers(self, request, context):
        metric = request.metric
        event_map = {
            'views': 'post_was_viewed',
            'likes': 'post_was_liked',
            'comments': 'post_was_commented'
        }
        event_type = event_map.get(metric)
        if not event_type:
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details(f'Unknown metric: {metric}')
            return stats_pb2.TopUsersResponse(users=[])

        query = """
            SELECT user_id, count() AS cnt
            FROM events
            WHERE event_type = %(event_type)s
            GROUP BY user_id
            ORDER BY cnt DESC
            LIMIT 10
        """
        rows = self.ch_client.execute(query, {'event_type': event_type})
        users = [stats_pb2.UserCount(user_id=str(row[0]), count=row[1]) for row in rows]
        return stats_pb2.TopUsersResponse(users=users)
