import psycopg2
import datetime
from datetime import timedelta
import uuid
from passlib.context import CryptContext
import base64
import re

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_encrypt(password):
    sample_string_bytes = password.encode("ascii")
    base64_bytes = base64.b64encode(sample_string_bytes)
    base64_string = base64_bytes.decode("ascii")
    return base64_string

connection = psycopg2.connect(database="postgres", user="postgres", password="Vettely417vzvvzv&", host="localhost", port=5432)

def check_input_is_correct(stroka):
    return bool(re.match(r'^[A-Za-z]+$|^\d+$',stroka))

def register(login, password, email):
    if not check_input_is_correct(login) or not check_input_is_correct(password) or not check_input_is_correct(email):
        return "Incorrect input."
    cursor = connection.cursor()
    now = datetime.datetime.now()
    try:
        password = get_password_encrypt(password)
        cursor.execute(f"INSERT INTO service_users (user_login, user_pass, user_email, created, modified) VALUES (\'{login}\', \'{password}\', \'{email}\', \'{str(now)}\', \'{str(now)}\');")
        connection.commit()
    except psycopg2.errors.UniqueViolation:
        connection.rollback()
        return "Current login already exists."
    return "User was registered."

def autenficate(login, password):
    if not check_input_is_correct(login) or not check_input_is_correct(password):
        return "Incorrect input."
    
    password = get_password_encrypt(password)
    print(password)
    cursor = connection.cursor()
    cursor.execute(f"SELECT user_id from service_users WHERE user_login = \'{login}\' and user_pass = \'{password}\';")
    connection.commit()
    result = cursor.fetchone()
    print(result)
    if result:
        token = uuid.uuid4()
        cursor.execute(f"UPDATE service_users SET access_token=\'{token}\', modified=\'{str(datetime.datetime.now())}\' where user_id = {result[0]};")
        connection.commit()
        return "Success, token: %s" % token
    return "A user with these login and password was not found."

def check_time(token):
    cursor = connection.cursor()
    cursor.execute(f"SELECT modified from service_users WHERE access_token = \'{token}\';")
    connection.commit()
    result = cursor.fetchone()
    print(result)
    
    format = '%Y-%m-%d %H:%M:%S.%f'
    modified = datetime.datetime.strptime(result[0], format)
    now = datetime.datetime.now()

    return now > modified + timedelta(minutes=5)

def create_new_token(token):
    if check_time(token):
        return "The token is expired. Create a new one using /get_new_token_login."
    new_token = uuid.uuid4()
    cursor = connection.cursor()
    cursor.execute(f"UPDATE service_users SET access_token=\'{new_token}\', modified=\'{str(datetime.datetime.now())}\' where access_token = \'{token}\';")
    connection.commit()
    return "New token: %s" % new_token

def create_new_token_login(login, password):
    password = get_password_encrypt(password)
    print(password)
    cursor = connection.cursor()
    cursor.execute(f"SELECT user_id from service_users WHERE user_login = \'{login}\' and user_pass = \'{password}\';")
    connection.commit()
    result = cursor.fetchone()
    print(result)
    if result:
        token = uuid.uuid4()
        cursor.execute(f"UPDATE service_users SET access_token=\'{token}\', modified=\'{str(datetime.datetime.now())}\' where user_id = {result[0]};")
        connection.commit()
        return "New token: %s" % token
    return "A user with these login and password was not found."

def get_info(token):
    if check_time(token):
        return "The token is expired. Create a new one using /get_new_token_login."
    cursor = connection.cursor()
    cursor.execute(f"SELECT * from service_users WHERE access_token = \'{token}\';")
    connection.commit()
    result = cursor.fetchone()
    return(result)

def update(field, value, token):
    if check_time(token):
        return "The token is expired. Create a new one using /get_new_token_login."
    if field in ['user_name', 'user_surname', 'user_email', 'user_birth']:
        cursor = connection.cursor()
        cursor.execute(f"UPDATE service_users SET {field}=\'{value}\', modified=\'{str(datetime.datetime.now())}\' where access_token = \'{token}\';")
        connection.commit()
        return "The field was updated."
    return "Field is not found. You can update only: user_name, user_surname, user_email and user_birth"
    
def get_user_id(token):
    cursor = connection.cursor()
    cursor.execute(f"SELECT user_id from service_users WHERE access_token = \'{token}\';")
    connection.commit()
    result = cursor.fetchone()
    return result[0]
    