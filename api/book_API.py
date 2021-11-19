from flask import Blueprint, render_template, jsonify, request, session, g
from flask.helpers import url_for
from sqlalchemy import func
from werkzeug.utils import redirect
from models.Book import Book
from models.BookBorrow import BookBorrow
from models.BookComment import BookComment
from db_connect import db
from datetime import datetime

book = Blueprint('book', __name__, url_prefix="/book")

@book.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    g.user_id = None if user_id is None else user_id

@book.route('/', methods=['GET'])
def book_list() :
    if session.get('user_id') :
        book_list = Book.query.all()
        return render_template('book.html', book_list=book_list)
    else :
        return redirect(url_for('index'))

@book.route('/<id>')
def book_detail(id) :

    book_data = Book.query.filter(Book.id == id).first()
    return render_template('book_detail.html',book_data=book_data)

@book.route('/borrow', methods=['GET','POST']) 
def book_borrow() :
    if request.method == 'GET':
        user_id = session.get('user_id')
        ratingQuery = db.session.query(BookComment.book_id, func.round(func.avg(BookComment.rating)).label('rating')).group_by(BookComment.book_id).subquery()

        borrow_list = db.session.query(Book.id, Book.book_name, BookBorrow.id.label('borrow_id'), BookBorrow.book_id, BookBorrow.borrow_date, BookBorrow.return_date, BookBorrow.return_flag) \
                    .join(BookBorrow, BookBorrow.book_id == Book.id) \
                    .outerjoin(ratingQuery, ratingQuery.c.book_id == Book.id) \
                    .filter(BookBorrow.user_id == user_id, BookBorrow.return_flag == 'T').all()

        return render_template('book_borrow.html', borrow_list=borrow_list)

    else :
        book_id = request.form.get('book_id')
        user_id = session.get("user_id")

        #책 재고 확인
        book_data = Book.query.filter(Book.id == book_id).first()
        if book_data.stock == 0 :
            jsonify(result='fail',message='대여 가능한 재고가 없습니다.')

        #같은책 대여는 x
        borrow_data = BookBorrow.query.filter((BookBorrow.book_id == book_id) & (BookBorrow.user_id == user_id) & (BookBorrow.return_flag == 'F')).first()
        if borrow_data is not None :
            return jsonify(result='fail', message="이미 대여한 도서입니다.")

        bb = BookBorrow(user_id, book_id)
        #트랜지션에서 에러가 났을경우
        try :
            book_data.stock -= 1
            db.session.add(bb)
            db.session.commit()
        except :
            db.session.rollback()
            return jsonify(result='fail', message="대여를 실패하였습니다. 관리자에게 문의 부탁드립니다.")

        #위 모든 로직이 통과되었을겨우에는 성공  
        return jsonify(result='success', message=f"대여하였습니다. 반납일은 {bb.return_due_date.strftime('%Y-%m-%d') } 까지입니다.")

@book.route('/return', methods=['GET','POST']) 
def book_return():
    if request.method == 'GET':
        user_id = session.get('user_id')
        #평점 가져오는 서브쿼리
        ratingQuery = db.session.query(BookComment.book_id, func.round(func.avg(BookComment.rating)).label('rating')).group_by(BookComment.book_id).subquery()

        borrow_list = db.session.query(Book.id, Book.book_name, BookBorrow.id.label('borrow_id'), BookBorrow.book_id, BookBorrow.borrow_date, BookBorrow.return_due_date, BookBorrow.return_flag) \
                    .join(BookBorrow, BookBorrow.book_id == Book.id) \
                    .outerjoin(ratingQuery, ratingQuery.c.book_id == Book.id) \
                    .filter(BookBorrow.user_id == user_id, BookBorrow.return_flag == 'F').all()
        
        return render_template('book_return.html', borrow_list=borrow_list)

    else :
        user_id = session.get('user_id')
        book_id = request.form.get('book_id')
        borrow_id = request.form.get('borrow_id')
        #반냡 flag T, 반납일자 오늘 날짜로
        try :
            borrow = BookBorrow.query.filter(BookBorrow.id == borrow_id, BookBorrow.user_id == user_id, BookBorrow.book_id == book_id, BookBorrow.return_flag == 'F').first()
            if borrow is None :
                return jsonify(result='fail', message='반납을 실패하였습니다. 관리자에게 문의 부탁드립니다.1')

            book = Book.query.filter(Book.id == book_id).first()
            if book is None :
                return jsonify(result='fail', message='반납을 실패하였습니다. 관리자에게 문의 부탁드립니다.2')

            borrow.return_flag = 'T'
            borrow.return_date = datetime.today().strftime('%Y-%m-%d')
            book.stock += 1
            db.session.commit()
        except :
            db.session.rollback()
            return jsonify(result='fail', message='반납을 실패하였습니다. 관리자에게 문의 부탁드립니다.3')

        return jsonify(result='success', message='반납을 완료하였습니다.')
