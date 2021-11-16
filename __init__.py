from flask import Flask, render_template

def create_app(test_config=None) :
    app = Flask(__name__, instance_relative_config=True)


    app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:root@127.0.0.1:3306/library"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    app.config.from_mapping(
        SECRET_KEY ='dev',
        JSON_AS_ASCII = False
    )

    @app.route('/')
    def index() :
        return render_template('index.html')

    return app