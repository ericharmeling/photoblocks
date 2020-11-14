from flask import request
from uuid import uuid4


def add_user(chain):
    user_name = request.form["user-name"]
    user_key = str(uuid4()).replace('-', '')
    user_data = {'user_name': user_name, 'user_key': user_key}

    chain.users.append(user_data)


def login_creds():
    user_name = request.form["user-name"]
    user_password = request.form["user-password"]
    private_key = request.form["private-key"]
    creds = {"user_name": user_name, "user_password": user_password, "private_key": private_key}
    return creds
