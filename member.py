import datetime
from datetime import date
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required
from sqlalchemy import func
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from forms import BookingForm, CheckInForm, CheckOutForm, MaintenanceRequestForm, TravelRequestForm, LoginForm, RegistrationForm,  enter_guest_idForm, BookingFormMember
from models import db, current_guest, Room, hospitality_staff, iitgn_member, Reservation, Bill,  maintenance_request, PastGuests, Feedback, travel_request, Assignment, RequiresMaintenance, ManagesMaintenance, ManagesReservation, IncursBill, Makes, GeneratesBill, InitiatedTravelRequest
from random import choices
import string

member = Blueprint('iitgn_member_dashboard', __name__)

@member.route('/iitgn_member_dashboard/new_booking', methods=['GET', 'POST'])
@login_required
def new_booking():

    form = BookingFormMember()
    highest_reservation_id = db.session.query(func.max(Reservation.reservation_id)).scalar()
    print(highest_reservation_id) 
    iitgn_id = current_user.get_id()

    if form.validate_on_submit():
        
        highest_reservation_id = db.session.query(func.max(Reservation.reservation_id)).scalar()

        new_reservation = Reservation(
            reservation_id = highest_reservation_id + 1,
            number_of_people = form.number_of_people.data,
            check_in_date = form.check_in_date.data,
            check_out_date = form.check_out_date.data,
            room_type = form.room_type.data,
            specially_enabled_room_required = form.specially_enabled_room_required.data,
            comments = form.comments.data,
            email_id = form.email_id.data,
            checked_in = False,
            checked_out = False,
            confirmed = False,
            iitgn_id = iitgn_id
        )
        db.session.add(new_reservation)
        db.session.commit()

        makes = Makes(
            reservation_id = new_reservation.reservation_id,
            iitgn_id = iitgn_id
        )
        db.session.add(makes)
        db.session.commit()

        flash(f'Booking Request made successfully! Reservation ID: {new_reservation.reservation_id}', 'success')
        return redirect(url_for('iitgn_member_dashboard.new_booking'))
    else:
        print(form.errors)
    return render_template('new_booking.html', form=form, iitgn_id=iitgn_id)