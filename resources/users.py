from flask.views import MethodView
from flask import request


# import db_config

# db_client = db(db_config.settings)


class UserRegisterResource(MethodView):
    def post(self):
        user_type = request.form["user-type"]
        user_name = request.form["user-name"]
        fields = [user_type, user_name]

        for field in fields:
            if not field:
                return "Invalid Data", 404

        # db_client.add_user(fields)

        return fields, 200


class UserLoginResource(MethodView):
    def post(self):
        user_name = request.form["user-name"]
        user_password = request.form["user-password"]
        private_key = request.form["private-key"]
        fields = [user_name, user_password, private_key]

        for field in fields:
            if not field:
                return "Invalid Data", 404

        # db_client.check_user(user_type, user_name)
        # server.login

        return fields, 200


class UserListResource(MethodView):
    def get(self):
        return db_client.users
