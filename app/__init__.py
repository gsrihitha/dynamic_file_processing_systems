from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(
        __name__,
        template_folder='../templates',
        static_folder='../static'
    )
    app.config['SECRET_KEY'] = 'replace-with-a-secure-key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    return app



