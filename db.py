from pymongo import MongoClient
from werkzeug.security import generate_password_hash
import ssl
from user import User

client=MongoClient("mongodb+srv://danleybjohn:JVKP0ueMv7LcGgeW@cluster0.yricu42.mongodb.net/?retryWrites=true&w=majority")

chat_db=client.get_database("Chatdb")
users_collection=chat_db.get_collection("users")

def save_user(username,email,password):
    pass_hash=generate_password_hash(password)
    users_collection.insert_one({'_id':username,'email':email,'password':pass_hash})


def get_user(username):
    user_data=users_collection.find_one({'_id':username})
    return User(user_data['_id'],user_data['email'],user_data['password']) if user_data else None

