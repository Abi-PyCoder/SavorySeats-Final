from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = "database.db"

def create_app():
    ap = Flask(__name__, template_folder='template', static_url_path='/static')
    ap.config['SECRET_KEY'] = 'ABI'
    ap.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(ap)



    from .routes import routes
    from .auth import auth

    ap.register_blueprint(routes, url_prefix = '/')
    ap.register_blueprint(auth, url_prefix = '/')

    from .models import User

    create_database(ap)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(ap)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return ap

def create_database(ap):
    if not path.exists('Website/' + DB_NAME):
        with ap.app_context():
            db.create_all()
        print('Created Database!')
