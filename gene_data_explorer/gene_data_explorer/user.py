from flask_login import UserMixin
from gene_data_explorer import db
from gene_data_explorer.models import Authorized_user_emails
from decimal import *
import itertools
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
        print(user, 'users.py')
        if user is None:
            return None
        print('continued')
        user = User(
            id_=user[0],
            username=user[1],
            email=user[2]
        )
        return user
    
    def create(self):
        print(creating)
        user = db.Model.classes.users(id=self.id, username=self.username, email=self.email)
        db.session.add(user)
        db.session.commit()

    def get_id(self):
        return str(self.id)

    @staticmethod
    def authorized_email(email):
        print('authorized_email')
        auth_emails = db.session.query(Authorized_user_emails.email).all()
        authorized= [item for t in auth_emails for item in t]
        print(authorized, 'auth_emails')
        if email in authorized:
            authed = True
        else:
            authed = False
        print('authed', authed)
        return authed