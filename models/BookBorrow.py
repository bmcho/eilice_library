from db_connect import db
from datetime import datetime, timedelta

class BookBorrow(db.Model) :
    __tablename__ = 'book_borrow'
    id = db.Column(db.Integer, primary_key=True, nullable=False,autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'))
    borrow_date = db.Column(db.Date, nullable=False, default=datetime.today().strftime('%Y-%m-%d'))
    return_due_date = db.Column(db.Date, nullable=False, default=(datetime.today() + timedelta(days=7)).strftime('%Y-%m-%d 23:59:59'))
    return_flag = db.Column(db.String(1), nullable=False, default='F')
    return_date = db.Column(db.Date, default = None)
    

    def __init__(self, user_id, book_id) :
        self.user_id = user_id
        self.book_id = book_id

