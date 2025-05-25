from fastapi import APIRouter, HTTPException, Query
import grpc
from technical_files.protos.generated import stats_pb2_grpc, stats_pb2

router = APIRouter(prefix='/stat_service', tags=['StatService'])

channel = grpc.insecure_channel('localhost:50051')
stub = stats_pb2_grpc.StatisticsServiceStub(channel)

@router.get("/stats/post/{post_id}")
def get_post_stats(post_id: str):
    try:
        request = stats_pb2.PostIdRequest(post_id=post_id)
        response = stub.GetPostStats(request)
        return {
            "views": response.views,
            "likes": response.likes,
            "comments": response.comments
        }
    except grpc.RpcError as e:
        raise HTTPException(status_code=500, detail=f"gRPC error: {e.details()}")

@router.get("/stats/post/{post_id}/views/dynamics")
def get_post_views_dynamics(post_id: str):
    try:
        request = stats_pb2.PostIdRequest(post_id=post_id)
        response = stub.GetPostViewsDynamics(request)
        return [{"date": entry.date, "views": entry.count} for entry in response.entries]
    except grpc.RpcError as e:
        raise HTTPException(status_code=500, detail=f"gRPC error: {e.details()}")

@router.get("/stats/post/{post_id}/likes/dynamics")
def get_post_likes_dynamics(post_id: str):
    try:
        request = stats_pb2.PostIdRequest(post_id=post_id)
        response = stub.GetPostLikesDynamics(request)
        return [{"date": entry.date, "likes": entry.count} for entry in response.entries]
    except grpc.RpcError as e:
        raise HTTPException(status_code=500, detail=f"gRPC error: {e.details()}")

@router.get("/stats/post/{post_id}/comments/dynamics")
def get_post_comments_dynamics(post_id: str):
    try:
        request = stats_pb2.PostIdRequest(post_id=post_id)
        response = stub.GetPostCommentsDynamics(request)
        return [{"date": entry.date, "comments": entry.count} for entry in response.entries]
    except grpc.RpcError as e:
        raise HTTPException(status_code=500, detail=f"gRPC error: {e.details()}")

@router.get("/stats/top/posts")
def get_top_posts(
    metric: str = Query(..., regex="^(likes|comments|views)$", description="Metric to sort by: likes, comments, or views")
):
    try:
        request = stats_pb2.TopPostsRequest(metric=metric)
        response = stub.GetTopPosts(request)
        return [{"post_id": post.post_id, metric: post.count} for post in response.posts]
    except grpc.RpcError as e:
        raise HTTPException(status_code=500, detail=f"gRPC error: {e.details()}")

@router.get("/stats/top/users")
def get_top_users(
    metric: str = Query(..., regex="^(likes|comments|views)$", description="Metric to sort by: likes, comments, or views")
):
    try:
        request = stats_pb2.TopUsersRequest(metric=metric)
        response = stub.GetTopUsers(request)
        return [{"user_id": user.user_id, metric: user.count} for user in response.users]
    except grpc.RpcError as e:
        raise HTTPException(status_code=500, detail=f"gRPC error: {e.details()}")