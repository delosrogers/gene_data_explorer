from flask_login import UserMixin
from gene_data_explorer import db
from decimal import *
class User(UserMixin):
    def __init__(self, id_, username, email):
        self.id = id_
        self.username = username
        self.email = email

    @staticmethod
    def get(user_id):
        print(user_id)
        users = db.Model.classes.users
        user = db.session.query(users.id, users.username, users.email).filter(users.id == Decimal(user_id)).first()
        print(user)
        if len(user)<3:
            return None
        print('continued')
        user = User(
            id_=user[0],
            username=user[1],
            email=user[2]
        )
        return user
    
    @staticmethod
    def create(id_, username, email):
        user = db.Model.classes.users(id=id_, username=username, email=email)
        db.session.add(user)
        db.session.commit()

    def get_id(self):
        return str(self.id)

