from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from forms import BookingForm, CheckInForm, CheckOutForm, MaintenanceRequestForm, TravelRequestForm, LoginForm, RegistrationForm
from models import db, current_guest, Room, hospitality_staff, iitgn_member, Reservation, Bill, HousekeepingStaff, MaintenanceRequest, PastGuests, Feedback, TravelRequest, Driver, Booking, Assignment, RequiresMaintenance, ManagesMaintenance, ManagesReservation, IncursBill, Makes, GeneratesBill, InitiatedTravelRequest

admin = Blueprint('hospitality_staff_dashboard', __name__)

@admin.route('/hospitality_staff_dashboard/booking', methods=['GET', 'POST'])
@login_required
def booking():
    form = BookingForm()
    if form.validate_on_submit():
        # Handle booking form submission
        flash('Reservation created successfully!', 'success')
        return redirect(url_for('hospitality_staff_dashboard/booking'))
    return render_template('booking.html', form=form)

@admin.route('/hospitality_staff_dashboard/check_in', methods=['GET', 'POST'])
@login_required
def check_in():
    form = CheckInForm()
    if form.validate_on_submit():
        # Handle check-in form submission
        flash('Guest checked in successfully!', 'success')
        return redirect(url_for('hospitality_staff_dashboard/check_in'))
    return render_template('check_in.html', form=form)

@admin.route('/hospitality_staff_dashboard/check_out', methods=['GET', 'POST'])
@login_required
def check_out():
    form = CheckOutForm()
    if form.validate_on_submit():
        # Handle check-out form submission
        flash('Guest checked out successfully!', 'success')
        return redirect(url_for('hospitality_staff_dashboard/check_out'))
    return render_template('check_out.html', form=form)

@admin.route('/hospitality_staff_dashboard/travel_request', methods=['GET', 'POST'])
@login_required
def travel_request():
    form = TravelRequestForm()
    if form.validate_on_submit():
        # Handle travel request form submission
        highest_id = db.session.query(db.func.max(TravelRequest.travel_request_id)).scalar()
        if highest_id is None:
            highest_id = 0
        travel_request = TravelRequest(
            travel_request_id=highest_id + 1,
            number_of_travellers=form.number_of_travellers.data,
            date_of_travel=form.date_of_travel.data,
            pick_up_time=form.pick_up_time.data,
            destination=form.destination.data,
            travel_purpose=form.travel_purpose.data
        )

        db.session.add(travel_request)
        db.session.commit()
        flash('Travel request submitted successfully!', 'success')
        return redirect(url_for('hospitality_staff_dashboard/travel_request'))
    return render_template('travel_request.html', form=form)

