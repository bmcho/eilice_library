from db_connect import db
from flask_login import UserMixin

class BookComment(db.model, UserMixin) :
    __tablename__ = 'book_comment'
    id = db.Column(db.Integer, primary_key=True, nullable=False,autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'))
    isbn = db.Column(db.Integer, db.ForeignKey('book.isbn'))
    comment = db.Column(db.String(200), nullable=False)
    rating = db.Column(db.Numeric, nullable=False)

    def __init__(self, user_id, book_id, isbn, comment, rating) :
        self.user_id = user_id
        self.book_id = book_id
        self.isbn = isbn
        self.comment = comment
        self.rating = rating

