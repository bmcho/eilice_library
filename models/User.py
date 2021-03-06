from sqlalchemy.orm import lazyload
from db_connect import db
from . import BookBorrow, BookComment

class User(db.Model) :
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    user_name = db.Column(db.String(100), nullable=False)
    user_pw = db.Column(db.String(200), nullable=False)
    user_nick = db.Column(db.String(100), nullable=False)

    FK_BookBorrow = db.relationship('BookBorrow', backref='user')
    FK_BookComment = db.relationship('BookComment', backref='user')

    def __init__(self, user_name, user_pw, user_nick) :
        self.user_name = user_name
        self.user_pw = user_pw
        self.user_nick = user_nick
        

