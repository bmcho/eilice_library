from flask import Blueprint, render_template, jsonify, request, session, g, json
from flask.helpers import url_for
from sqlalchemy import func
import sqlalchemy
from werkzeug.utils import redirect
from models.Book import Book
from models.User import User
from models.BookBorrow import BookBorrow
from models.BookComment import BookComment
from db_connect import db
from datetime import datetime
from math import ceil
from flask_restful import Api, Resource

book = Blueprint('book', __name__, url_prefix="/book")
api = Api(book)

@book.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    if user_id :
        g.user_id = user_id
    else :
        g.user_id = None

# class BookSearch(Resource):
#     def get(self) :
#         if session.get('user_id') :
#             page = int(request.args.get('page', 1))
#             bookname = request.args.get('name')
#             limit = 8
#             totalPage = ceil(db.session.query(func.count(Book.id).label("book_count")).first().book_count/8)

#             if totalPage == 0 :
#                 totalPage = 1 
#             elif page >= totalPage :
#                 page = totalPage
#             offset = (page-1) * limit

#             ratingQuery = db.session.query(BookComment.book_id, func.cast(func.round(func.avg(BookComment.rating)), sqlalchemy.Integer).label('rating')).group_by(BookComment.book_id).subquery()

#             book_list = db.session.query(Book.id, Book.book_name, Book.stock, ratingQuery.c.book_id, ratingQuery.c.rating) \
#                         .outerjoin(ratingQuery, ratingQuery.c.book_id == Book.id).offset(offset).limit(limit).all()

#             return jsonify(result="success", book_list=[(dict(row)) for row in book_list])
#             # return render_template('book_list.html', book_list=book_list, page=page, totalPage=totalPage)
#         else :
#             return redirect(url_for('index'))

# api.add_resource(BookSearch, '/')

#도서 메인페이지
@book.route('/', methods=['GET'])
def book_list() :
    if session.get('user_id') :
        page = int(request.args.get('page', 1))
        limit = 8
        totalPage = ceil(db.session.query(func.count(Book.id).label("book_count")).first().book_count/8)

        if totalPage == 0 :
            totalPage = 1 
        elif page >= totalPage :
            page = totalPage
        offset = (page-1) * limit

        ratingQuery = db.session.query(BookComment.book_id, func.cast(func.round(func.avg(BookComment.rating)), sqlalchemy.Integer).label('rating')).group_by(BookComment.book_id).subquery()

        book_list = db.session.query(Book.id, Book.book_name, Book.stock, ratingQuery.c.book_id, ratingQuery.c.rating) \
                    .outerjoin(ratingQuery, ratingQuery.c.book_id == Book.id).offset(offset).limit(limit).all()

        return render_template('book_list.html', book_list=book_list, page=page, totalPage=totalPage)

    else :
        return redirect(url_for('index'))

#책 상세 페이지
#댓글등록,삭제
@book.route('/detail', methods=['GET','POST','DELETE'])
def book_detail() :
    if session.get('user_id') :
        if request.method == 'GET' :
            id = request.args.get('id')
            book_data = Book.query.filter(Book.id == id).first()
            comment_data = db.session.query(BookComment.id, BookComment.user_id, BookComment.comment, BookComment.rating, User.user_name).join(User, BookComment.user_id == User.id).filter(BookComment.book_id == id).order_by(BookComment.comment_date.desc()).all()

            return render_template('book_detail.html',book_data=book_data, comment_data=comment_data)

        elif request.method == 'POST' :
            user_id = session.get("user_id")    
            book_id = request.form.get('book_id')
            comment = request.form.get('comment')
            rating = request.form.get('rating')

            try :
                db.session.add(BookComment(user_id, book_id, comment, rating))
                db.session.commit()
                return jsonify(result='success', message='댓글이 성공적으로 작성되었습니다.')
            except Exception as ex:
                print(ex)
                db.session.rollback()
                return jsonify(result='fail', message='댓글작성에 실패하였습니다. 관리자에게 문의바랍니다.')

        elif request.method == 'DELETE' :
            id = request.form.get("id")    
            user_id = session.get("user_id")    
            try :
                deleteData = BookComment.query.filter(BookComment.id == id, BookComment.user_id == user_id).first()
                db.session.delete(deleteData)
                db.session.commit()
                return jsonify(result='success', message='댓글이 성공적으로 삭제되었습니다.')
            except Exception as ex:
                print(ex)
                db.session.rollback()
                return jsonify(result='fail', message='댓글삭제에 실패하였습니다. 관리자에게 문의바랍니다.')

    else :
        return redirect(url_for('index'))
        
#대여기록 페이지
@book.route('/borrow', methods=['GET','POST']) 
def book_borrow() :
    if session.get('user_id') :
        if request.method == 'GET':
            user_id = session.get('user_id')
            ratingQuery = db.session.query(BookComment.book_id, func.cast(func.round(func.avg(BookComment.rating)), sqlalchemy.Integer).label('rating')).group_by(BookComment.book_id).subquery()

            borrow_list = db.session.query(Book.id, Book.book_name, BookBorrow.id.label('borrow_id'), BookBorrow.book_id, BookBorrow.borrow_date, BookBorrow.return_date, BookBorrow.return_flag, ratingQuery.c.book_id, ratingQuery.c.rating) \
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
            except Exception as ex:
                print(ex)
                db.session.rollback()
                return jsonify(result='fail', message="대여를 실패하였습니다. 관리자에게 문의 부탁드립니다.")

            #위 모든 로직이 통과되었을겨우에는 성공  
            return jsonify(result='success', message=f"대여하였습니다. 반납일은 {bb.return_due_date.strftime('%Y-%m-%d') } 까지입니다.")
    else :
        return redirect(url_for('index')) 

#반납페이지
@book.route('/return', methods=['GET','POST']) 
def book_return():
    if session.get('user_id') :
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
            except Exception as ex:
                print(ex)
                db.session.rollback()
                return jsonify(result='fail', message='반납을 실패하였습니다. 관리자에게 문의 부탁드립니다.3')

            return jsonify(result='success', message='반납을 완료하였습니다.')
    else :
        return redirect(url_for('index')) 
