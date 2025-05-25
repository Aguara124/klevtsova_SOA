from fastapi import FastAPI, HTTPException, Response
import requests
import uvicorn

import db.db_user as db_user
from kafka_producer import KafkaProducer

from fastapi import APIRouter

router = APIRouter(prefix='/user_service', tags=['UserService'])
kafka_producer = KafkaProducer()

@router.post("/register")
async def register_user(login: str, password: str, email: str, response:Response):
    print("Received ", login, password, email)
    text = db_user.register(login, password, email)
    if text == "Current login already exists.":
        response.status_code = 400
    kafka_producer.send_user_registered_event(db_user.get_user_id_cred(login, password), login, email)
    return text

@router.post("/authentificate")
async def authentificate(login: str, password: str, response:Response):
    print("Received ", login, password)
    text = db_user.autenficate(login, password)
    if text == "A user with these login and password was not found.":
        response.status_code = 401
    return text
    
@router.get("/get_new_token")
async def get_token(token: str, response:Response):
    print("Received ", token)
    text =  db_user.create_new_token(token)
    if text == "The token is expired. Create a new one using /get_new_token_login.":
        response.status_code = 401
    return text

@router.get("/get_new_token_with_login")
async def get_token_login(login: str, password:str, response:Response):
    print("Received ", login, password)
    text =  db_user.create_new_token_login(login, password)
    if text == "A user with these login and password was not found.":
        response.status_code = 401
    return text

@router.get("/get_info")
async def get_info(token: str, response:Response):
    text =  db_user.get_info(token)
    if text == "The token is expired. Create a new one using /get_new_token_login.":
        response.status_code = 401
    return text

@router.post("/update")
async def update_profile(field: str, value:str, token: str, response:Response):
    print("Received ", field, value, token)
    text = db_user.update(field, value, token)
    if text == "Field is not found. You can update only: user_name, user_surname, user_email and user_birth":
        response.status_code = 400
    elif text == "The token is expired. Create a new one using /get_new_token_login.":
        response.status_code = 401
    return text

