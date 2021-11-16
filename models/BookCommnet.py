from db_connect import db
from flask_login import UserMixin

class BookComment(db.model, UserMixin) :
    __tablename__ = 'book_comment'
    id = db.Column(db.Integer, primary_key=True, nullable=False,autoincrement=True)
    isbn = db.Column(db.String(30), db.ForeignKey('book.isbn'))
    user_id = db.Column(db.String(30), db.ForeignKey('user.user_id'))
    comment = db.Column(db.String(200), nullable=False)
    rating = db.Column(db.Numeric, nullable=False)

    def __init__(self, isbn, user_id, comment, rating) :
        self.isbn = isbn
        self.user_id = user_id
        self.comment = comment
        self.rating = rating

