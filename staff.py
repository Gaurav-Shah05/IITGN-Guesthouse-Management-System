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

@staff.route('/housekeeping_staff_dashboard/close/<int:request_id>', methods=['GET','POST'])
@login_required
def close(request_id):
    maintenance_request_close = maintenance_request.query.get_or_404(request_id)
    maintenance_request_close.status = 'closed'
    db.session.commit()
    flash('Maintenance request closed successfully!', 'success')
    return redirect(url_for('housekeeping_staff_dashboard.view'))

@staff.route('/housekeeping_staff_dashboard/view', methods=['GET', 'POST'])
@login_required
def view():
    staff_id = current_user.get_id();
    requests = maintenance_request.query.filter_by(housekeeping_staff_id = staff_id, status="open").all()
    return render_template('housekeeping_maintenance_request_closed.html', assigned = requests)