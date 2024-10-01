from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from datetime import datetime


class User(db.Model,UserMixin):
        id= db.Column(db.Integer,primary_key=True)
        email_id=db.Column(db.String(30),nullable=False,unique=True)
        reg_no=db.Column(db.String(20),nullable=False,unique=True)
        password_hash=db.Column(db.String(30),nullable=False)
        name=db.Column(db.String(30),nullable=False,)

        def set_password(self,password):
            self.password_hash=generate_password_hash(password)
        def check_password(self,password):
            return check_password_hash(self.password_hash,password)
        
class AttendanceRecord(db.Model):
     id=db.Column(db.Integer,primary_key=True)
     user_id= db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)
     type= db.Column(db.String(10))
     timestamp=db.Column(db.DateTime, default=datetime.utcnow)
     
