from pymongo import MongoClient
from bson import ObjectId
from dotenv import load_dotenv
import os
from werkzeug.security import generate_password_hash, check_password_hash
load_dotenv()


def init_db():
    uri = os.environ.get("MONGO_URI")

    if not uri:
        raise ValueError("MONGO_URI is not configured.")

    client = MongoClient(uri)

    db = client["FlaskApp-Docker"]

    return db


def get_items(db):
    return [
        {
            "_id": str(doc["_id"]),
            "name": doc["name"]
        }
        for doc in db.items.find()
    ]


def add_item(db, data):
    result = db.items.insert_one({
        "name": data["name"]
    })

    return {
        "inserted_id": str(result.inserted_id)
    }


def delete_item(db, item_id):
    db.items.delete_one({
        "_id": ObjectId(item_id)
    })

    return {
        "status": "deleted"
    }
def register_user(db, username, password):
    existing_user = db.users.find_one({
        "username": username
    })

    if existing_user:
        return {
            "error": "Username already exists"
        }

    password_hash = generate_password_hash(password)

    result = db.users.insert_one({
        "username": username,
        "password": password_hash
    })

    return {
        "message": "User registered successfully",
        "user_id": str(result.inserted_id)
    }
def login_user(db, username, password):
    user = db.users.find_one({
        "username": username
    })

    if not user:
        return {
            "error": "Invalid username or password"
        }

    if not check_password_hash(user["password"], password):
        return {
            "error": "Invalid username or password"
        }

    return {
        "message": "Login successful",
        "username": user["username"]
    }
from werkzeug.security import generate_password_hash, check_password_hash


def register_user(db, username, password):
    existing_user = db.users.find_one({
        "username": username
    })

    if existing_user:
        return {
            "error": "Username already exists"
        }

    result = db.users.insert_one({
        "username": username,
        "password": generate_password_hash(password)
    })

    return {
        "user_id": str(result.inserted_id),
        "message": "User registered successfully"
    }


def login_user(db, username, password):
    user = db.users.find_one({
        "username": username
    })

    if not user:
        return {
            "error": "Invalid username or password"
        }

    if not check_password_hash(user["password"], password):
        return {
            "error": "Invalid username or password"
        }

    return {
        "message": "Login successful",
        "user_id": str(user["_id"])
    }