from flask import Blueprint, render_template, jsonify, request, redirect, flash, session, g
from flask.helpers import url_for
from models.User import User
from db_connect import db
from flask_bcrypt import Bcrypt

user = Blueprint('user', __name__)
bcrypt = Bcrypt()

@user.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    g.user_id = None if user_id is None else user_id

@user.route('/signin', methods=['GET','POST']) 
def signin():
    if request.method == 'GET' :
        if session.get("user_id") is not None :
            return redirect(url_for('index'))
        else :
            return render_template('signin.html')
    else :
        print("확인")
        user_name = request.form.get('user_name')
        user_pw = request.form.get('user_pw')
        user = User.query.filter(User.user_name == user_name).first()
        message,messageType = None, None
        
        if user is not None :
            if bcrypt.check_password_hash(user.user_pw, user_pw):
                session['user_id'] = user.id
                return jsonify(result='success')
            else :
                message,messageType = 'ID 혹은 비밀번호를 잘못 입력하셨거나 등록되지 않은 ID 입니다.', 'warning'
                flash(message=message, category=messageType)
                return jsonify(result="fail")

@user.route('/signout')
def signout() :
    session.clear()
    return redirect(url_for('index'))


@user.route('/signup', methods=['GET','POST'])
def signup() :
    if request.method == 'GET' :
        return render_template('signup.html')
    else :
        user_name = request.form.get('user_name')
        user_pw = request.form.get('user_pw')

        message,messageType = None, None
        #user_name체크
        data = User.query.filter(User.user_name == user_name).first()

        if data is not None :
            message,messageType = '해당 아이디는 이미 가입되어있는 아이디입니다.', 'warning'
            flash(message=message, category=messageType)
            return jsonify(result="fail")

        pw_hash = bcrypt.generate_password_hash(user_pw)

        addUser = User(user_name, pw_hash)
        db.session.add(addUser)
        db.session.commit()
        return jsonify(result="success")
