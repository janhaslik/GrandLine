from sqlalchemy import create_engine, text
from sqlalchemy.exc import IntegrityError
import bcrypt

DB_NAME = "grand_line"

connection_string = f'mysql+mysqlconnector://root:root123!@127.0.0.1:3306/{DB_NAME}'
engine = create_engine(connection_string)
connection = engine.connect()

# INIT TABLES

user_table = text("create table if not exists users("
                  "id int primary key auto_increment,"
                  "username varchar(255) unique,"
                  "email varchar(255) unique,"
                  "salt varchar(255),"
                  "hash varchar(255)"
                  ");")

model_table = text("create table if not exists models("
                   "id int primary key auto_increment,"
                   "model_name varchar(255),"
                   "model_type varchar(255),"
                   "data_path varchar(255),"
                   "user_id int,"
                   "foreign key (user_id) references users(id)"
                   ");");

# TODO: Implement model type
"""
model_types_table = text("create table if not exists model_types("
                         "id int primary key auto_increment,"
                         "model_type varchar(255);")
"""

connection.execute(user_table)
# connection.execute(model_types_table)
connection.execute(model_table)


def insert_user(username, email, password):
    # SALT * HASH
    salt = bcrypt.gensalt()
    generated_hash = bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

    statement = text("INSERT INTO users(username, email, salt, hash) VALUES(:username, :email, :salt, :hash);")

    try:
        connection.execute(statement,
                           {"username": username, "email": email, "salt": salt.decode('utf-8'), "hash": generated_hash})
        connection.commit()

        # Retrieve the last inserted id
        result = connection.execute(text("select last_insert_id()")).fetchone()
        return {"status": "success"}
    except IntegrityError as e:
        print(f"IntegrityError: {e}")
        return {"status": "fail", "message": "User already exists"}
    except Exception as e:
        print(f"Exception: {e}")
        return {"status": "fail", "message": "An error occurred"}


def login_user(username_email, password):
    statement = text("SELECT id, hash, salt FROM users WHERE username = :username_email OR email = :username_email;")
    result = connection.execute(statement, {"username_email": username_email}).fetchone()

    if result is None:
        return {"status": "fail", "message": "User does not exist"}

    user_id, stored_hash, stored_salt = result
    if bcrypt.checkpw(password.encode('utf-8'), stored_hash.encode('utf-8')):
        return {"status": "success", "user_id": user_id}
    else:
        return {"status": "fail", "message": "Wrong password"}


def insert_model(model_name, model_type, data_path, user_id):
    statement = text(
        "INSERT INTO models(model_name, model_type, data_path, user_id) VALUES(:model_name, :model_type, :data_path, :user_id)")

    try:
        connection.execute(statement, {"model_name": model_name, "model_type": model_type, "data_path": data_path,
                                       "user_id": user_id})
        connection.commit()
        # Retrieve the last inserted id
        result = connection.execute(text("select last_insert_id()")).fetchone()
        return result[0]
    except Exception as e:
        print(e)
        return 403


def get_model(model_id):
    statement = text("SELECT model_type, data_path FROM models WHERE id = :model_id")

    try:
        result = connection.execute(statement, {"model_id": model_id}).fetchone()
        return result
    except Exception as e:
        print(e)
        return 403
