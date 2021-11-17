from flask import Flask, render_template
from db_connect import db
from flask_login import LoginManager

from models.User import User

def create_app(test_config=None) :
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_mapping(
        SECRET_KEY ='dev',
        JSON_AS_ASCII = False
    )

    app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:root@127.0.0.1:3306/library"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    from .api import user_API
    app.register_blueprint(user_API.user)

    @app.route('/')
    def index() :
        return render_template('index.html')

    return app