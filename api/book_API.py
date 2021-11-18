from flask import Blueprint, render_template, jsonify, request, session, g
from models.Book import Book
from db_connect import db
from sqlalchemy.exc import IntegrityError
from datetime import datetime

from models.BookBorrow import BookBorrow

book = Blueprint('book', __name__, url_prefix="/book")

@book.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    g.user_id = None if user_id is None else user_id

@book.route('/', methods=['GET'])
def book_list() :
    if request.method == 'GET' :
        book_list = Book.query.all()
        return render_template('book.html', book_list=book_list)

@book.route('/<id>')
def book_detail(id) :

    book_data = Book.query.filter(Book.id == id).first()
    print(book_data.id)
    return render_template('book_detail.html',book_data=book_data)

@book.route('borrow', methods=['POST']) 
def book_borrow() :
    book_id = request.form.get('book_id')
    user_id = session.get("user_id")

    book_data = Book.query.filter(Book.id == book_id).first()
    if book_data.stock == 0 :
        jsonify(result='fail',message='대여 가능한 수량이 없습니다.')

    bb = BookBorrow(user_id, book_id)
    try :
        book_data.stock -= 1
        db.session.add(bb)
        db.session.commit()
    except IntegrityError :
        return jsonify(result='success', message="대여를 실패하였습니다. 관리자에게 문의 부탁드립니다.")
    
    return jsonify(result='success', message=f"대여하였습니다. 반납일은 {bb.return_date.strftime('%Y-%m-%d') } 까지입니다.")
