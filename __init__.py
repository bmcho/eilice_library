from datetime import timedelta
from flask import Flask, redirect, session
from flask.helpers import url_for
from db_connect import db

import os

def create_app(test_config=None) :
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_mapping(
        SECRET_KEY = os.environ.get('SECRET_KEY'),
        SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI'),
        SQLALCHEMY_TRACK_MODIFICATIONS = 'False',
        JSON_AS_ASCII = False
    )

    db.init_app(app)

    from .api import user_API, book_API
    app.register_blueprint(user_API.user)
    app.register_blueprint(book_API.book)

    @app.before_request
    def before_request():
        session.permanent = True
        app.permanent_session_lifetime = timedelta(minutes=10)

    @app.route('/')
    def index() :
        user_id = session.get('user_id')
        print(user_id)
        if user_id is not None :
            return redirect(url_for('book.book_list', page=1))
        else :
            return redirect(url_for('user.signin'))

    return app