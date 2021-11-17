from db_connect import db
from . import BookBorrow, BookCommnet

class User(db.Model) :
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    user_name = db.Column(db.String(100), nullable=False)
    user_pw = db.Column(db.String(200), nullable=False)

    FK_BookBroow = db.relationship('BookBorrow', backref='user')
    FK_BookCommnet = db.relationship('BookComment', backref='user')

    def __init__(self, user_name, user_pw) :
        self.user_name = user_name
        self.user_pw = user_pw

