from flask import Blueprint, render_template, request, redirect
from flask_login import login_user,login_required,logout_user,current_user
from .models import db,AttendanceRecord

views=Blueprint('views',__name__)

@views.route('/home')
def home():
  return render_template('home.html')

@views.route('/analytics', methods=['GET'])
@login_required
def analytics():
    user_id = current_user.id
    arrival_count = AttendanceRecord.query.filter_by(user_id=user_id, type='arrival').count()
    late_arrival_count = AttendanceRecord.query.filter_by(user_id=user_id, type='late_arrival').count()
    early_departure_count = AttendanceRecord.query.filter_by(user_id=user_id, type='early_departure').count()
    departure_count = AttendanceRecord.query.filter_by(user_id=user_id, type='departure').count()

    return render_template('analytics.html', 
                           user=current_user, 
                           departure_count=departure_count,
                           arrival_count=arrival_count, 
                           late_arrival_count=late_arrival_count, 
                           early_departure_count=early_departure_count)

