import datetime
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from forms import BookingForm, CheckInForm, CheckOutForm, MaintenanceRequestForm, TravelRequestForm, LoginForm, RegistrationForm, enter_guest_idForm, billForm, ChangePasswordFirst, ChangePassword, FeedbackForm
from models import db, current_guest, Room, hospitality_staff, iitgn_member, Reservation, Bill, housekeeping_staff, maintenance_request, PastGuests, Feedback, travel_request, driver, Assignment, RequiresMaintenance, ManagesMaintenance, ManagesReservation, IncursBill, Makes, GeneratesBill, InitiatedTravelRequest
from sqlalchemy.orm import joinedload
from sqlalchemy import select

guest = Blueprint('current_guest_dashboard', __name__)

@guest.route('/current_guest_dashboard/first_login', methods=['GET', 'POST'])
@login_required
def first_login():

    guest_id = current_user.get_id() 
    guest = current_guest.query.filter_by(guest_id=guest_id).first()

    form = ChangePasswordFirst()
    if form.validate_on_submit():
        guest.password = form.new_password.data
        guest.first_login = False
        db.session.commit()
        flash('Password changed successfully!', 'success')
        return redirect(url_for('current_guest_dashboard'))

    return render_template('first_login.html', form=form)

@guest.route('/current_guest_dashboard/change_password', methods=['GET', 'POST'])
@login_required
def change_password():

    guest_id = current_user.get_id()
    guest = current_guest.query.filter_by(guest_id=guest_id).first()

    form = ChangePassword()
    if form.validate_on_submit():
        guest.password = form.new_password.data
        db.session.commit()
        flash('Password changed successfully!', 'success')
        return redirect(url_for('current_guest_dashboard'))

    return render_template('change_password.html', form=form)

@guest.route('/current_guest_dashboard/guest_travel_request', methods=['GET', 'POST'])
@login_required
def guest_travel_request():
    form = TravelRequestForm()
    if form.validate_on_submit():
        # Handle travel request form submission
        # Acquire lock on the travel_request table
        locked_table = select(travel_request).with_for_update()
        db.session.execute(locked_table)


        with db.session.begin_nested():
            highest_id = db.session.query(db.func.max(travel_request.travel_request_id)).scalar()
            if highest_id is None:
                highest_id = 0
            travel_request_add = travel_request(
                travel_request_id=highest_id + 1,
                number_of_travellers=form.number_of_travellers.data,
                date_of_travel=form.date_of_travel.data,
                pick_up_time=form.pick_up_time.data,
                destination=form.destination.data,
                travel_purpose=form.travel_purpose.data
            )
            db.session.add(travel_request_add)
            db.session.flush()  # Flush to generate the primary key before adding the initiated_travel_request
            initiated_travel_request = InitiatedTravelRequest(
                travel_request_id=highest_id + 1,
                guest_id=current_user.get_id()
            )
            db.session.add(initiated_travel_request)
        db.session.commit()
        flash('Travel request submitted successfully!', 'success')
        return redirect(url_for('current_guest_dashboard.guest_travel_request'))
    return render_template('guest_travel_request.html', form=form)

@guest.route('/current_guest_dashboard/feedback', methods=['GET', 'POST'])
@login_required
def feedback(): 
    form = FeedbackForm()
    if form.validate_on_submit():
        # Handle feedback form submission
        highest_id = db.session.query(db.func.max(Feedback.feedback_id)).scalar()
        if highest_id is None:
            highest_id = 0
        feedback = Feedback(
            feedback_id=highest_id + 1,
            feedback=form.feedback.data,
            star_rating=form.star_rating.data,
            date = datetime.datetime.now().date(),
            guest_id=current_user.get_id()
        )

        db.session.add(feedback)
        db.session.commit()
        flash('Feedback submitted successfully!', 'success')
        return redirect(url_for('current_guest_dashboard.feedback'))
    return render_template('guest_feedback.html', form=form)


@guest.route('/current_guest_dashboard/guest_maintenance_request', methods=['GET', 'POST'])
@login_required
def guest_maintenance_request():
    form = MaintenanceRequestForm()
    if form.validate_on_submit():
        # Handle travel request form submission
       
       
        locked_table = select(maintenance_request).with_for_update()
        db.session.execute(locked_table)
       
        with db.session.begin_nested():
            highest_id = db.session.query(db.func.max(maintenance_request.request_id)).scalar()
            if highest_id is None:
                highest_id = 0
            maintenancerequest = maintenance_request(
                request_id=highest_id + 1,
                description=form.description.data,
                status = 'open',
                date_created = datetime.datetime.now().date(),
                time_created = datetime.datetime.now().time(),        
               
                housekeeping_staff_id = None
            )
            db.session.add(maintenancerequest)
        db.session.commit()
        flash('Maintenance request submitted successfully!', 'success')
        return redirect(url_for('current_guest_dashboard.guest_maintenance_request'))
    return render_template('guest_maintenance_request.html', form=form)


@guest.route('/current_guest_dashboard/show_bills')
@login_required
def show_bills():
    g_id = current_user.get_id()
    incurs_bills = IncursBill.query.filter(IncursBill.guest_id == g_id).all()
    bill_id = incurs_bills.bill_id
    all_paid_bills = Bill.query.filter_by(bill_id=bill_id, paid_status='1').all()
    total_amount = sum(bill_entry.amount for bill_entry in all_paid_bills)
    #all_paid_bills = db.session.query(Bill).join(IncursBill, IncursBill.bill_id == Bill.bill_id).filter(IncursBill.guest_id == current_user.id, Bill.paid_status == True).all()
    
    '''
    all_unpaid_bills = db.session.query(Bill).join(IncursBill, IncursBill.bill_id == Bill.bill_id).filter(IncursBill.guest_id == current_user.guest_id, Bill.paid_status == False).all()
    all_paid_bills = db.session.query(Bill).join(IncursBill, IncursBill.bill_id == Bill.bill_id).filter(IncursBill.guest_id == current_user.guest_id, Bill.paid_status == True).all()
    '''
    
    #if all_paid_bills:
    #    total_amount = sum(bill_entry.amount for bill_entry in all_paid_bills)
        #flash(f'Bill generated successfully! for guest_id = {guest_id}', 'success')
        #return render_template('bill_entries.html', bill_entries=bill_entries, total_amount=total_amount)
        
    return render_template('show_bills.html', total_amount=total_amount, all_paid_bills=all_paid_bills)