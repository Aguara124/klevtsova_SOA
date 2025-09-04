from fastapi import FastAPI, HTTPException, Response
import requests
import uvicorn
import grpc
import db.db_user as db_user
import db.db_posts as db_posts
from grpc_files import Posts_pb2, Posts_pb2_grpc
import json

from kafka_producer import KafkaProducer

from fastapi import APIRouter

channel = grpc.insecure_channel('localhost:50051')
stub = Posts_pb2_grpc.SocialNetworkServiceStub(channel)

router = APIRouter(prefix='/posts', tags=['Posts'])

kafka_producer = KafkaProducer()

@router.post("/create_post")
async def create_post(token, title, is_private, description, tags, resp:Response):
    if db_user.check_time(token) == True:
        resp.status_code = 401
        return "The token is expired. Create a new one using /get_new_token_login."
    creator_id = db_user.get_user_id(token)
    response = stub.CreatePost(Posts_pb2.CreatePostRequest(title=title, description = description, creator_id = creator_id, is_private = bool(is_private), tags = tags))
    dictionary = {"post_id":response.post_id, "message": response.message}
    return json.dumps(dictionary)

@router.post("/delete_post")
async def delete_post(token, post_id, resp:Response):
    if db_user.check_time(token) == True:
        response.status_code = 401
        return "The token is expired. Create a new one using /get_new_token_login."
    response = stub.DeletePost(Posts_pb2.DeletePostRequest(post_id=int(post_id)))
    print(response)
    if response.message == "Post not found":
        resp.status_code == 401
    dictionary = {"post_id":response.post_id, "message": response.message}
    return json.dumps(dictionary)

@router.post("/get_post_by_id")
async def get_post_by_id(token, post_id, resp:Response):
    if db_user.check_time(token) == True:
        resp.status_code = 401
        return "The token is expired. Create a new one using /get_new_token_login."
    response = stub.GetPostById(Posts_pb2.GetPostByIdRequest(post_id=int(post_id)))
    dictionary = {"post_id":response.post.id, "title": response.post.title, "creator_id":response.post.creator_id, "is_private":response.post.is_private, "tags":response.post.tags, "creation_date":response.post.creation_date, "update_date":response.post.update_date}
    if response.post.id == 0:
        print("HERE")
        resp.status_code = 401
        return "Post with id %s was not found."%post_id
    
    kafka_producer.send_post_viewed_event(post_id, db_user.get_user_id(token))
    
    return json.dumps(dictionary)

@router.post("/update_post")
async def delete_post(token, post_id, title, is_private, description, tags, resp:Response):
    if db_user.check_time(token) == True:
        resp.status_code = 401
        return "The token is expired. Create a new one using /get_new_token_login."
    response = stub.UpdatePost(Posts_pb2.UpdatePostRequest(post_id=int(post_id), title=title, description = description, is_private = bool(is_private), tags = tags))
    print(response)
    if response.message == "Post not found":
        resp.status_code == 401
        return "Post with id %s was not found."%post_id
    dictionary = {"post_id":response.post_id, "message": response.message}
    return json.dumps(dictionary)

@router.post("/get_posts_list")
async def get_posts_list(token, resp:Response):
    if db_user.check_time(token) == True:
        response.status_code = 401
        return "The token is expired. Create a new one using /get_new_token_login."
    
    response = stub.GetPostsList(Posts_pb2.Empty())
    print(response.posts)
    posts = {}
    count = 1
    for post in response.posts:
        dictionary = {"post_id":post.id, "title": post.title, "creator_id":post.creator_id, "is_private":post.is_private, "tags":post.tags, "creation_date":post.creation_date, "update_date":post.update_date}
        posts["Post %s"%count] = dictionary
        count+=1
    return json.dumps(posts)

# ------ New methods just for sending to kafka ----------------

@router.post("/comment_post")
async def comment_post(token, post_id, comment, resp:Response):
    if db_user.check_time(token) == True:
        resp.status_code = 401
        return "The token is expired. Create a new one using /get_new_token_login."
    if db_posts.get_post_by_id(post_id) == False:
        resp.status_code = 400
        return "This post does not exist"
    user_id = db_user.get_user_id(token)
    kafka_producer.send_post_viewed_event(post_id, user_id)
    kafka_producer.send_post_commented_event(post_id, user_id, comment)
    return "Test Kafka"

@router.post("/like_post")
async def comment_post(token, post_id, resp:Response):
    if db_user.check_time(token) == True:
        resp.status_code = 401
        return "The token is expired. Create a new one using /get_new_token_login."
    if db_posts.get_post_by_id(post_id) == False:
        resp.status_code = 400
        return "This post does not exist"
    user_id = db_user.get_user_id(token)
    kafka_producer.send_post_viewed_event(post_id, user_id)
    kafka_producer.send_post_liked_event(post_id, user_id)
    return "Test Kafka"
    