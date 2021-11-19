from db_connect import db
from . import BookBorrow, BookComment

class Book(db.Model) :
    __tablename__ = 'book'
    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    isbn = db.Column(db.String(13), nullable=False)
    book_name = db.Column(db.String(100), nullable=False)
    publisher = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    publication_date = db.Column(db.String(10), nullable=False)
    page = db.Column(db.Integer)
    description = db.Column(db.String(2000))
    link = db.Column(db.String(200))
    image_url = db.Column(db.String(100))
    stock = db.Column(db.Integer)

    FK_BookBorrow = db.relationship('BookBorrow', backref='book')
    FK_BookComment = db.relationship('BookComment', backref='book')

    def __init__(self, isbn, book_name, publisher, author, publication_date, page, description, link, image_url, stock) :
        self.isbn = isbn
        self.book_name = book_name
        self.publisher = publisher
        self.author = author
        self.publication_date = publication_date
        self.page = page
        self.description = description
        self.link = link
        self.image_url = image_url
        self.stock = stock

    def book_rating(self):
        return round(sum(Comment.rating for Comment in self.FK_BookComment)/len(self.FK_BookComment)) if len(self.FK_BookComment) != 0 else 0
