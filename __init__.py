from datetime import timedelta
from flask import Flask, redirect, session
from flask.helpers import url_for
from db_connect import db

import dotenv
import os

dotenv.load_dotenv('.env')

def create_app(test_config=None) :
    app = Flask(__name__, instance_relative_config=True)

    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URI')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    from api import user_API, book_API
    app.register_blueprint(user_API.user)
    app.register_blueprint(book_API.book)

    @app.before_request
    def before_request():
        session.permanent = True
        app.permanent_session_lifetime = timedelta(minutes=10)

    @app.route('/')
    def index() :
        user_id = session.get('user_id')
        if user_id is not None :
            return redirect(url_for('book.book_list', page=1))
        else :
            return redirect(url_for('user.signin'))

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host='0.0.0.0', port=80, debug=False)