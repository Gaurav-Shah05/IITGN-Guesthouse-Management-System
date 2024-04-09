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

Driver = Blueprint('driver_dashboard', __name__)

@Driver.route('/driver_dashboard/view', methods=['GET', 'POST'])
@login_required
def view():
    driver_license = current_user.get_id();
    requests = travel_request.query.filter_by(driver_license = driver_license).all()
    # select requests whose date_of_travel is after today
    requests = [request for request in requests if request.date_of_travel >= date.today()]
    return render_template('travel_request_view.html', assigned = requests)