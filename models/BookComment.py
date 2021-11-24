from db_connect import db
from datetime import datetime

class BookComment(db.Model) :
    __tablename__ = 'book_comment'
    id = db.Column(db.Integer, primary_key=True, nullable=False,autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'))
    comment = db.Column(db.String(200), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    comment_date = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, user_id, book_id, comment, rating) :
        self.user_id = user_id
        self.book_id = book_id
        self.comment = comment
        self.rating = rating

