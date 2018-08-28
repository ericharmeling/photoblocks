# users.py -- might want to rename this or the users.py resource --
# Defines the User class, a data structure for registered users


class User:
    def __init__(self, user_type, user_name, public_key, private_key):
        self.user_type = user_type
        self.user_name = user_name
        self.public_key = public_key
        self.private_key = private_key


class Miner(User):
    def __init__(self, nodes):
        self.nodes = nodes
