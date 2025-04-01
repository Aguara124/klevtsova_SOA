from fastapi import FastAPI, HTTPException, Response
import requests
import uvicorn
import grpc
import db.db_user as db_user
import db.db_posts as db_posts
from grpc_files import Posts_pb2, Posts_pb2_grpc
import json

from fastapi import APIRouter

channel = grpc.insecure_channel('localhost:50051')
stub = Posts_pb2_grpc.SocialNetworkServiceStub(channel)

router = APIRouter(prefix='/posts', tags=['Posts'])

@router.post("/create_post")
async def create_post(token, title, is_private, description, tags, response:Response):
    creator_id = db_user.get_user_id(token)
    print(creator_id)
    print(tags)
    if db_user.check_time(token) == True:
        response.status_code = 401
        return "The token is expired. Create a new one using /get_new_token_login."
    response = stub.CreatePost(Posts_pb2.CreatePostRequest(title=title, description = description, creator_id = creator_id, is_private = bool(is_private), tags = tags))
    dictionary = {"post_id":response.post_id, "message": response.message}
    return json.dumps(dictionary)
    
# @router.get("/get_new_token")
# async def get_token(token: str, response:Response):
#     print("Received ", token)
#     text =  db_user.create_new_token(token)
#     if text == "The token is expired. Create a new one using /get_new_token_login.":
#         response.status_code = 401
#     return text

# @router.get("/get_new_token_with_login")
# async def get_token_login(login: str, password:str, response:Response):
#     print("Received ", login, password)
#     text =  db_user.create_new_token_login(login, password)
#     if text == "A user with these login and password was not found.":
#         response.status_code = 401
#     return text

# @router.get("/get_info")
# async def get_info(token: str, response:Response):
#     text =  db_user.get_info(token)
#     if text == "The token is expired. Create a new one using /get_new_token_login.":
#         response.status_code = 401
#     return text

# @router.post("/update")
# async def update_profile(field: str, value:str, token: str, response:Response):
#     print("Received ", field, value, token)
#     text = db_user.update(field, value, token)
#     if text == "Field is not found. You can update only: user_name, user_surname, user_email and user_birth":
#         response.status_code = 400
#     elif text == "The token is expired. Create a new one using /get_new_token_login.":
#         response.status_code = 401
#     return text