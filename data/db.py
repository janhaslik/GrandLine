from sqlalchemy import create_engine, text
from sqlalchemy.exc import IntegrityError
import bcrypt

DB_NAME = "grand_line"

connection_string = f'mysql+mysqlconnector://root:root123!@127.0.0.1:3306/{DB_NAME}'
engine = create_engine(connection_string)


# INIT TABLES
def init():
    with engine.connect() as connection:
        user_table = text("create table if not exists users("
                          "id int primary key auto_increment,"
                          "username varchar(255) unique,"
                          "email varchar(255) unique,"
                          "salt varchar(255),"
                          "hash varchar(255)"
                          ");")

        model_types_table = text("create table if not exists model_types("
                                 "id int primary key auto_increment,"
                                 "model_type varchar(255) unique"
                                 ");")

        model_table = text("create table if not exists models("
                           "id int primary key auto_increment,"
                           "model_name varchar(255),"
                           "model_type_id int,"
                           "data_path varchar(255),"
                           "status enum('deployed', 'not deployed'),"
                           "user_id int,"
                           "foreign key (model_type_id) references model_types(id),"
                           "foreign key (user_id) references users(id)"
                           ");")

        connection.execute(user_table)
        connection.execute(model_types_table)
        connection.execute(model_table)

        try:
            static_types_statement = text("insert into model_types(model_type) values('ARIMA'),('LSTM');")
            connection.execute(static_types_statement)
        except Exception as e:
            connection.rollback()
            pass

init()


def insert_model(model_name, model_type, data_path, user_id):
    with engine.connect() as connection:
        try:
            # Check if model_type exists in model_types table
            model_type_result = connection.execute(text("SELECT id FROM model_types WHERE model_type = :model_type"),
                                                   {"model_type": model_type}).fetchone()
            if model_type_result:
                model_type_id = model_type_result[0]
            else:
                # If model_type doesn't exist, return an error
                return {"status": "fail", "message": "Model type does not exist in the lookup table"}

            # Insert model with model_type_id
            statement = text("INSERT INTO models(model_name, model_type_id, data_path, status, user_id) "
                             "VALUES(:model_name, :model_type_id, :data_path, :status, :user_id)")

            connection.execute(statement, {"model_name": model_name, "model_type_id": model_type_id,
                                           "data_path": data_path, "status": "not deployed", "user_id": user_id})
            connection.commit()
            # Retrieve the last inserted id
            result = connection.execute(text("select last_insert_id()")).fetchone()
            return {"status": "success", "model_id": result[0]}
        except IntegrityError as e:
            connection.rollback()
            print(f"IntegrityError: {e}")
            return {"status": "fail", "message": "Model insertion failed"}
        except Exception as e:
            connection.rollback()
            print(f"Exception: {e}")
            return {"status": "fail", "message": "An error occurred during model insertion"}


def deploy_model(model_id):
    with engine.connect() as connection:
        statement_exists = text("select * from models where id = :model_id")
        model_exists_result = connection.execute(statement_exists, {"model_id": model_id})

        if not model_exists_result:
            return {"status": "fail", "message": "Model not found"}

        statement_deploy = text("update models set status = 'deployed' where id = :model_id")
        connection.execute(statement_deploy, {"model_id": model_id})
        connection.commit()

        return {"status": "success"}


def insert_user(username, email, password):
    # Generate salt and hash the password
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)

    with engine.connect() as connection:
        try:
            # Insert user data into the database
            statement = text(
                "INSERT INTO users(username, email, salt, hash) VALUES(:username, :email, :salt, :hashed_password)")
            connection.execute(statement, {"username": username, "email": email, "salt": salt.decode('utf-8'),
                                           "hashed_password": hashed_password.decode('utf-8')})
            connection.commit()
            return {"status": "success"}
        except IntegrityError as e:
            connection.rollback()
            print(f"IntegrityError: {e}")
            return {"status": "fail", "message": "User already exists"}
        except Exception as e:
            connection.rollback()
            print(f"Exception: {e}")
            return {"status": "fail", "message": "An error occurred during user insertion"}


def login_user(username_email, password):
    with engine.connect() as connection:
        statement = text("SELECT id, hash, salt FROM users WHERE username = :username_email OR email = :username_email;")
        result = connection.execute(statement, {"username_email": username_email}).fetchone()

        if result is None:
            return {"status": "fail", "message": "User does not exist"}

        user_id, stored_hash, stored_salt = result
        if bcrypt.checkpw(password.encode('utf-8'), stored_hash.encode('utf-8')):
            return {"status": "success", "user_id": user_id}
        else:
            return {"status": "fail", "message": "Wrong password"}


def get_model(model_id):
    with engine.connect() as connection:
        statement = text(
            "SELECT model_type, data_path FROM models inner join model_types on model_types.id=models.model_type_id WHERE models.id = :model_id")

        try:
            result = connection.execute(statement, {"model_id": model_id}).fetchone()
            return result
        except Exception as e:
            print(e)
            return 403


def get_models(userid):
    with engine.connect() as connection:
        statement = text(
            "select models.id, model_name, model_type, status FROM models inner join model_types on model_types.id=models.model_type_id WHERE user_id = :userid")

        try:
            result = connection.execute(statement, {"userid": userid}).fetchall()
            if len(result) == 0:
                return 404

            models = [{"id": id, "model_name": model_name, "model_type": model_type, "status": status} for
                      id, model_name, model_type, status in result]

            return models
        except Exception as e:
            print(e)
            return 403

def delete_model(model_id, userid):
    with engine.connect() as connection:
        statement_exists = text("select * from models where id = :model_id and user_id = :userid")
        model_exists_result = connection.execute(statement_exists, {"model_id": model_id, 'user_id': userid})

        if not model_exists_result:
            return {"status": "fail", "message": "Model not found"}

        statement_delete = text("delete from models where id = :model_id and user_id = :userid")
        connection.execute(statement_delete, {"model_id": model_id, 'user_id': userid})
        connection.commit()

        return {"status": "success"}


def get_model_types():
    with engine.connect() as connection:
        statement = text("select model_type from model_types")
        try:
            result = connection.execute(statement).fetchall()
            if len(result) == 0:
                return 404

            model_types = [{"model_type": model_type} for model_type in result]

            return model_types
        except Exception as e:
            print(e)
            return 403