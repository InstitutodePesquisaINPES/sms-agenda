from flask_login import UserMixin

class User(UserMixin):
    def __init__(self, user_id, username, cpf, sus, password, user_type):
        self.id = user_id
        self.username = username
        self.cpf = cpf
        self.sus = sus
        self.password = password
        self.user_type = user_type


        from flask_sqlalchemy import SQLAlchemy

