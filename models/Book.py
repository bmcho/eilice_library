from db_connect import db
from flask_login import UserMixin


class Book(db.Model) :
    __tablename__ = 'book'
    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    isbn = db.Column(db.Integer, primary_key=True, nullable=False)
    book_name = db.Column(db.String(200), nullable=False)
    publisher = db.Column(db.String(200), nullable=False)
    author = db.Column(db.String(200), nullable=False)
    publication_date = db.Column(db.Date, nullable=False)
    page = db.Column(db.Integer)
    description = db.Column(db.String(1000))
    link = db.Column(db.String(200))

    FK_BookBroow = db.relationship('BookBorrow', backref='book')
    FK_BookCommnet = db.relationship('BookComment', backref='book')

    def __init__(self, isbn, book_name, publisher, author, publication_date, page, description, link) :
        self.isbn = isbn
        self.book_name = book_name
        self.publisher = publisher
        self.author = author
        self.publication_date = publication_date
        self.publication_date = publication_date
        self.page = page
        self.description = description
        self.link = link

