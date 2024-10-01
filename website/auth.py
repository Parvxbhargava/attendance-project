from flask import Blueprint, render_template, request, redirect,flash,url_for,Flask
from flask_login import login_user,login_required,logout_user,current_user
from flask_sqlalchemy import SQLAlchemy
from . import db
from .models import User

auth=Blueprint('auth',__name__)

@auth.route('/',methods=['GET','POST'])
def sign_up():

  if request.method=='POST':
    name=request.form.get('name')
    email=request.form.get('email')
    reg_no=request.form.get('regNo')
    password=request.form.get('password')
    confirm_password=request.form.get('confirmPassword')
    user_byregno=User.query.filter_by(reg_no=reg_no).first()
    if user_byregno:
      flash("user already exists",category="error")
      return redirect(url_for("auth.sign_up"))

    

    if password !=confirm_password:
      flash('Password Confirmation incorrect',category='error')
      return redirect(url_for('auth.sign_up')) 
       
    else:
      new_user=User(name=name,email_id=email,reg_no=reg_no,)
      new_user.set_password(password)
      db.session.add(new_user)
      db.session.commit()
      login_user(new_user,remember=True)
      return redirect(url_for('views.home'))

  return render_template('sign_up.html',user=current_user)


@auth.route("/login",methods=['GET','POST'])
def login():
  if request.method=='POST':
    regNo=request.form.get('regNo')
    password=request.form.get('password')
    user = User.query.filter_by(reg_no=regNo).first()
    if user:
      if user and user.check_password(password):
        login_user(user,remember=True)
        return redirect(url_for('views.home'))
      else:
        flash('Incorrect password,try again',category='error')
    else:
      flash('User does not exist',category='error')
    

  return render_template("login.html",user=current_user)

@auth.route('/logout')
@login_required
def logout():
  logout_user()
  return redirect(url_for('auth.login'))



