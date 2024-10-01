from flask import Flask,request
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, LoginManager
from os import path
from flask_mail import Mail


db=SQLAlchemy()

def createApp():
    
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///database.db'
    app.config['SECRET_KEY'] = 'ABC'
    

    db.init_app(app)

    login_manager=LoginManager(app)
    login_manager.login_view='auth.login'
    login_manager.init_app(app)
    

    from .attendance import attendance
    app.register_blueprint(attendance,url_prefix='/attendance')

    from .views import views
    app.register_blueprint(views, url_prefix='/')

    from .auth import auth
    app.register_blueprint(auth,url_prefix='/')

    
    @login_manager.user_loader
    def load_user(user_id):
        from .models import User
        return User.query.get(int(user_id)) 
    create_database(app)

    
   
   
    


    return app
def create_database(app):
    if not path.exists('website/database.db'):
        with app.app_context():
            db.create_all()
        print('created database')

