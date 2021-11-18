from flask import Flask, render_template, redirect, session
from flask.helpers import url_for
from db_connect import db

def create_app(test_config=None) :
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_mapping(
        SECRET_KEY ='dev',
        JSON_AS_ASCII = False
    )

    app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:root@127.0.0.1:3306/library"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    from .api import user_API, book_API
    app.register_blueprint(user_API.user)
    app.register_blueprint(book_API.book)

    @app.route('/')
    def index() :
        user_id = session.get('user_id')
        print(user_id)
        if user_id is not None :
            return redirect(url_for('book.book_list'))
        else :
            return redirect(url_for('user.signin'))

    return app