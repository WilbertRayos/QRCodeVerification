from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = "admin123"
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/slb'
    app.config['UPLOAD_FOLDER'] = 'static/qrcodes'
    db.init_app(app)


    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")

    from .models import Users

    login_manager = LoginManager()

    login_manager.login_view = "auth.login"

    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return Users.query.get(int(id))



    return app
