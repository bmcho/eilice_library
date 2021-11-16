from typing import DefaultDict
from db_connect import db
from flask_login import UserMixin
from datetime import datetime

class BookBorrow(db.model, UserMixin) :
    __tablename__ = 'book_borrow'
    id = db.Column(db.Integer, primary_key=True, nullable=False,autoincrement=True)
    user_id = db.Column(db.String(30), db.ForeignKey('user.user_id'))
    book_id = db.Column(db.String(30), db.ForeignKey('book.id'))
    isbn = db.Column(db.String(30), db.ForeignKey('book.isbn'))
    borrow_date = db.Column(db.Date, nullable=False, default= datetime.date.today().isoformat())
    return_date = db.Column(db.Date, nullable=False, default= datetime.date.today().isoformat() + datetime.timedelta(days=7))
    return_flag = db.Column(db.String(1), nullable=False, default='F')

    def __init__(self, isbn, user_id, comment, rating) :
        self.isbn = isbn
        self.user_id = user_id
        self.comment = comment
        self.rating = rating

