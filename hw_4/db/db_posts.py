import psycopg2
import datetime
from datetime import timedelta
import uuid
from passlib.context import CryptContext
import base64
import re

connection = psycopg2.connect(database="postgres", user="postgres", password="Vettely417vzvvzv&", host="localhost", port=5432)

def check_input_is_correct(stroka):
    return bool(re.match(r'^[A-Za-z]+$|^\d+$',stroka))

def create_post(title,  creator_id, is_private, description = "", tags=""):
    if not check_input_is_correct(title) or not check_input_is_correct(description):
        return "Incorrect input."
    cursor = connection.cursor()
    now = datetime.datetime.now()
    cursor.execute(f"INSERT INTO posts (title, creator_id, is_private, tags, creation_date, update_date) VALUES (\'{title}\', \'{creator_id}\', \'{is_private}\', \'{','.join(tags)}\', \'{str(now)}\', \'{str(now)}\') RETURNING id;")
    inserted_id = cursor.fetchone()[0]
    connection.commit()
    return inserted_id

def delete_post(post_id):
    try:
        cursor = connection.cursor()
        if get_post_by_id(post_id) == None:
            return False
        cursor.execute(f"DELETE FROM posts WHERE id = \'{post_id}\'")
        connection.commit()
        return True
    except:
        return False
    
def update_post(post_id, title, description, tags, is_private):
    print("Here")
    if not check_input_is_correct(title) or not check_input_is_correct(description):
        return "Incorrect input."
    cursor = connection.cursor()
    try:
        if get_post_by_id(post_id) == None:
            print("Not found")
            return False
        print("POST ID" , post_id)
        cursor.execute(f"UPDATE posts SET title=\'{title}\', description=\'{description}\', tags=\'{tags}\', is_private=\'{is_private}\', update_date=\'{str(datetime.datetime.now())}\' WHERE id = \'{post_id}\';")
        connection.commit()
        return True
    except: return False
    
def get_post_by_id(post_id):
    try:
        cursor = connection.cursor()
        cursor.execute(f"SELECT * from posts WHERE id = \'{post_id}\';")
        connection.commit()
        result = cursor.fetchone()
        return(result)
    except:
        return False

def get_posts_list():
    cursor = connection.cursor()
    cursor.execute(f"SELECT * from posts;")
    result = cursor.fetchall()
    return(result)

def get_last_index():
    try:
        cursor = connection.cursor()
        cursor.execute(f"SELECT id from posts ORDER BY id DESC LIMIT 1;")
        result = cursor.fetchone()
        return(result[0])
    except:
        return False