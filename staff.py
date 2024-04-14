import datetime
from datetime import date
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required
from sqlalchemy import func
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from forms import BookingForm, CheckInForm, CheckOutForm, MaintenanceRequestForm, TravelRequestForm, LoginForm, RegistrationForm,  enter_guest_idForm
from models import db, current_guest, Room, hospitality_staff, housekeeping_staff, iitgn_member, Reservation, Bill,  maintenance_request, PastGuests, Feedback, travel_request, Assignment, RequiresMaintenance, ManagesMaintenance, ManagesReservation, IncursBill, Makes, GeneratesBill, InitiatedTravelRequest
from random import choices
import string

staff = Blueprint('housekeeping_staff_dashboard', __name__)

#----------------- 

@staff.route('/housekeeping_staff_dashboard/close_other_request/<int:request_id>', methods=['GET','POST'])
@login_required
def close_other_request(request_id):
    maintenance_request_close = maintenance_request.query.get_or_404(request_id)
    maintenance_request_close.status = 'closed'
    db.session.commit()
    flash('Maintenance request closed successfully!', 'success')
    return redirect(url_for('housekeeping_staff_dashboard.view_other_request'))

@staff.route('/housekeeping_staff_dashboard/view_other_request', methods=['GET', 'POST'])
@login_required
def view_other_request():
    staff_id = current_user.get_id();
    requests = maintenance_request.query.filter_by(housekeeping_staff_id = staff_id, status="open").all()
    # select request from reqeusts whose request_id not in requires_maintenance table
    other_requests = []
    for request in requests:
        if not RequiresMaintenance.query.filter_by(request_id = request.request_id).first():
            other_requests.append(request)

    return render_template('housekeeping_maintenance_other_request_closed.html', assigned = other_requests)

@staff.route('/housekeeping_staff_dashboard/close_room_request/<int:request_id>', methods=['GET','POST'])
@login_required
def close_room_cleaning_request(request_id):
    maintenance_request_close = maintenance_request.query.get_or_404(request_id)
    maintenance_request_close.status = 'closed'
    #delete the corresponding entry from requires_maintenance table
    requires_maintenance = RequiresMaintenance.query.filter_by(request_id = request_id).first()
    db.session.delete(requires_maintenance)
    db.session.commit()
    flash('Maintenance request closed successfully!', 'success')
    return redirect(url_for('housekeeping_staff_dashboard.view_room_cleaning_request'))

@staff.route('/housekeeping_staff_dashboard/view_room_request', methods=['GET', 'POST'])
@login_required
def view_room_cleaning_request():
    staff_id = current_user.get_id();
    requests = maintenance_request.query.filter_by(housekeeping_staff_id = staff_id, status="open").all()
    # select request from reqeusts whose request_id in requires_maintenance table
    room_cleaning_requests = []
    for request in requests:
        if RequiresMaintenance.query.filter_by(request_id = request.request_id).first():
            room_cleaning_requests.append(request)
    return render_template('housekeeping_maintenance_room_request_closed.html', assigned = room_cleaning_requests)

#-----------------