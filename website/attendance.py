from flask import Blueprint,request,redirect,url_for,render_template,flash
from flask_login import login_required,current_user
from .models import db,AttendanceRecord
from datetime import datetime,time
from flask_mail import Mail,Message


attendance=Blueprint('attendance',__name__)

@attendance.route('/mark_presence',methods=['POST'])
@login_required
def mark_presence():
  flash("Presence marked",category='success')
  time_str=request.form.get('time')
  timestamp=datetime.strptime(time_str,'%H:%M')
  late_cutoff=time(22,0)
  is_late=timestamp.time()>late_cutoff
  new_record=AttendanceRecord(user_id=current_user.id,type='arrival',timestamp=timestamp)
  db.session.add(new_record)
  db.session.commit()
  if is_late:
       
     late_record = AttendanceRecord(user_id=current_user.id,type='late_arrival',timestamp=timestamp)
     db.session.add(late_record)
     db.session.commit()
    
  return redirect(url_for('views.home'))

@attendance.route('/depart',methods=['POST'])
@login_required
def depart():
  flash("Departure marked",category='success')
  time_str=request.form.get('time')
  timestamp=datetime.strptime(time_str,'%H:%M')
  early_cutoff=time(5,0)
  departing_early=timestamp.time()<early_cutoff
  new_record=AttendanceRecord(user_id=current_user.id,type='departure',timestamp=timestamp)
  db.session.add(new_record)
  db.session.commit()
  if departing_early:
    early_record=AttendanceRecord(user_id=current_user.id,type='early_departure',timestamp=timestamp)
    db.session.add(early_record)
    db.session.commit()
  return redirect(url_for('views.home'))


