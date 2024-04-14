import datetime
from datetime import date
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required
from sqlalchemy import func
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from forms import BookingForm, billForm, CheckInForm, CheckOutForm, MaintenanceRequestForm, TravelRequestForm, LoginForm, RegistrationForm,  enter_guest_idForm
from models import db, driver, current_guest, Room, hospitality_staff, housekeeping_staff, iitgn_member, Reservation, Bill,  maintenance_request, PastGuests, Feedback, travel_request, Assignment, RequiresMaintenance, ManagesMaintenance, ManagesReservation, IncursBill, Makes, GeneratesBill, InitiatedTravelRequest
from random import choices
import string
from sqlalchemy import select


admin = Blueprint('hospitality_staff_dashboard', __name__)


# @admin.route('/hospitality_staff_dashboard/check_in', methods=['GET', 'POST'])
# @login_required
# def check_in():

#     today = date.today()
#     reservations = Reservation.query.filter(Reservation.check_in_date == today, Reservation.checked_in == False).all()

#     if request.method == 'POST':
#         if 'add_guest' in request.form:
#             reservation_id = request.form['reservation_id']
#             reservation = Reservation.query.get(reservation_id)

#             highest_id = db.session.query(db.func.max(current_guest.guest_id)).scalar()

#             form = CheckInForm()
#             if form.validate_on_submit():
#                 guest = current_guest(
#                     guest_id=highest_id + 1,
#                     first_name=form.first_name.data,
#                     last_name=form.last_name.data,
#                     age=form.age.data,
#                     street=form.street.data, 
#                     state=form.state.data,
#                     pincode= form.pincode.data,    
#                     country=form.country.data,
#                     phone_no=form.phone_no.data,
#                     guest_category=form.guest_category.data,
#                     visit_purpose=form.visit_purpose.data,
#                     iitgn_id=form.iitgn_id.data,  # Do something  about it!
#                     email_id=form.email_id.data,
#                     phone_number=form.phone_number.data,
#                     reservation_id=reservation_id
#                 )
#                 db.session.add(guest)
#                 db.session.commit()
#                 flash('Guest added successfully!', 'success')
#                 if reservation.number_of_people > len(reservation.guests):
#                     if len(reservation.guests) % 2 == 0:
#                         return redirect(url_for('hospitality_staff_dashboard.room_assignment', reservation_id=reservation_id))
#                     return redirect(url_for('hospitality_staff_dashboard.check_in'))
#                 else:
#                     return redirect(url_for('hospitality_staff_dashboard.room_assignment', reservation_id=reservation_id))

#         elif 'assign_room' in request.form:
#             reservation_id = request.form['reservation_id']
#             room_id = request.form['room_id']
#             reservation = Reservation.query.get(reservation_id)
#             room = Room.query.get(room_id)
#             wifi_password = ''.join(choices(string.ascii_letters + string.digits, k=8))
#             for guest in reservation.guests:
#                 guest.room_id = room_id
#                 guest.wifi_password = wifi_password
#                 assignment = Assignment(reservation_id=reservation_id, room_id=room_id, wifi_password=wifi_password)
#                 db.session.add(assignment)
#             db.session.commit()
#             flash(f'Successful Assignment! WiFi Password: {wifi_password}', 'success')
#             return redirect(url_for('hospitality_staff_dashboard.check_in'))

#         elif 'finish_check_in' in request.form:
#             reservation_id = request.form['reservation_id']
#             reservation = Reservation.query.get(reservation_id)
#             reservation.checked_in = True
#             db.session.commit()
#             flash('Successful Check-In!', 'success')
#             return redirect(url_for('hospitality_staff_dashboard'))

#     return render_template('check_in.html', reservations=reservations)

# @admin.route('/hospitality_staff_dashboard/room_assignment/<int:reservation_id>', methods=['GET', 'POST'])
# @login_required
# def room_assignment(reservation_id):

#     reservation = Reservation.query.get_or_404(reservation_id)
#     available_rooms = Room.query.filter(
#         Room.room_type == reservation.room_type,
#         ~Room.room_no.in_([a.room_no for a in Assignment.query.all()])
#     ).all()

#     if request.method == 'GET':
#         reservation = Reservation.query.get_or_404(reservation_id)
#         available_rooms = Room.query.filter(
#             Room.room_type == reservation.room_type,
#             ~Room.id.in_([a.room_id for a in Assignment.query.all()])
#         ).all()
#         return render_template('room_assignment.html', reservation=reservation, available_rooms=available_rooms)

#     if request.method == 'POST':
#         room_id = request.form['room_id']
#         room = Room.query.get(room_id)
#         wifi_password = ''.join(choices(string.ascii_letters + string.digits, k=8))
#         for guest in reservation.guests:
#             guest.room_id = room_id
#             guest.wifi_password = wifi_password
#             assignment = Assignment(reservation_id=reservation_id, room_id=room_id, wifi_password=wifi_password)
#             db.session.add(assignment)
#         db.session.commit()
#         flash(f'Successful Assignment! WiFi Password: {wifi_password}', 'success')
#         return redirect(url_for('hospitality_staff_dashboard.check_in'))

#     return render_template('room_assignment.html', reservation=reservation, available_rooms=available_rooms)
    

# ROUTES FOR CHECK-IN

@admin.route('/hospitality_staff_dashboard/check_in', methods=['GET'])
@login_required
def check_in():

    today = date.today()
    reservations = Reservation.query.filter(Reservation.check_in_date == today, Reservation.checked_in == False, Reservation.confirmed == True).all()
    return render_template('check_in.html', reservations=reservations)

# Use this route to add guests to the reservation

@admin.route('/hospitality_staff_dashboard/add_guest/<int:reservation_id>/guest1', methods=['GET', 'POST'])
@login_required
def add_guest_1(reservation_id):

    reservation = Reservation.query.filter_by(reservation_id=reservation_id).first()
    no_of_guests = reservation.number_of_people
    print(no_of_guests)
    highest_id = db.session.query(db.func.max(current_guest.guest_id)).scalar()

    form = CheckInForm() 

    if form.validate_on_submit():
        highest_id = db.session.query(db.func.max(current_guest.guest_id)).scalar()
        highest_id = 0 if highest_id is None else highest_id
        print(highest_id)
        guest = current_guest(
            guest_id=highest_id + 1,
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            age=form.age.data,
            street=form.    street.data, 
            state=form.state.data,
            pincode= form.pincode.data,    
            country=form.country.data,
            phone_no=form.phone_no.data,
            guest_category=form.guest_category.data,
            visit_purpose=form.visit_purpose.data,
            iitgn_id=reservation.iitgn_id,  
            email_id=form.email_id.data,
            first_login=1
        )
        print(guest.first_name)
        db.session.add(guest)
        db.session.commit()
        flash(f'Guest 1 added successfully! Guest ID: {highest_id + 1}', 'success')
        if no_of_guests == 1:
            return redirect(url_for('hospitality_staff_dashboard.choose_room', reservation_id=reservation_id, guest_id = highest_id + 1))
        else:
            return redirect(url_for('hospitality_staff_dashboard.add_guest_2', reservation_id=reservation_id, guest_1_id=highest_id + 1))
    else:
        print(form.errors)
        

    return render_template('add_guest.html', form=form, no_of_guests=no_of_guests, reservation_id=reservation_id)

# Use this route to add guests to the reservation if the number of guests is more than 1

# Should few details like address and visit_purpose copied from guest 1 if both are related ??   

@admin.route('/hospitality_staff_dashboard/add_guest/<int:reservation_id>/guest2/<int:guest_1_id>', methods=['GET', 'POST'])
@login_required
def add_guest_2(reservation_id,guest_1_id):

    reservation = Reservation.query.filter_by(reservation_id=reservation_id).first()
    highest_id = guest_1_id 
    form = CheckInForm() 

    if form.validate_on_submit():
       
        guest = current_guest(
            guest_id=highest_id + 1,
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            age=form.age.data,
            street=form.street.data, 
            state=form.state.data,
            pincode= form.pincode.data,    
            country=form.country.data,
            phone_no=form.phone_no.data,
            guest_category=form.guest_category.data,
            visit_purpose=form.visit_purpose.data,
            iitgn_id=reservation.iitgn_id, 
            email_id=form.email_id.data,
            first_login=1
        )
        print(guest.first_name)
        db.session.add(guest)
        db.session.commit()
        guest_id = guest_1_id
        flash(f'Guest 2 added successfully! Guest ID: {highest_id + 1}', 'success')
        return redirect(url_for('hospitality_staff_dashboard.choose_room', reservation_id=reservation_id, guest_id = guest_id))

    return render_template('additional_guest.html', form=form, reservation_id=reservation_id, guest_1_id=guest_1_id)

@admin.route('/hospitality_staff_dashboard/choose_room/<int:reservation_id>/<int:guest_id>', methods=['GET', 'POST'])
@login_required
def choose_room(reservation_id,guest_id):
    
    reservation = Reservation.query.filter_by(reservation_id=reservation_id).first()
    print(reservation)
    no_of_guests = reservation.number_of_people
    print(reservation.room_type)
    available_rooms = Room.query.filter(
        Room.room_type == reservation.room_type,
        Room.is_specially_enabled == reservation.specially_enabled_room_required,
        ~Room.room_no.in_([a.room_no for a in Assignment.query.all()])
    ).all()

#------------------
    # select room from available_rooms whose room_no is not in room_no of RequiresMaintenance table
    available_rooms = [room for room in available_rooms if room.room_no not in [maintenance.room_no for maintenance in RequiresMaintenance.query.all()]]
#------------------

    print(available_rooms)
    
    guest_ids = []
    guest_ids.append(guest_id)
    if no_of_guests == 2:
        guest_ids.append(guest_id + 1)

    if request.method == 'POST':
        room_no = request.form['room_no']
        wifi_password = ''.join(choices(string.ascii_letters + string.digits, k=8))
        for guest_id in guest_ids:
            guest = current_guest.query.get(guest_id)
            guest.room_no = room_no
            guest.password = wifi_password
        assignment = Assignment(reservation_id=reservation_id, room_no=room_no, wifi_password=wifi_password)
        db.session.add(assignment)
        reservation.checked_in = True
        reservation.checked_out = False
        db.session.commit()
        flash(f'Checked In! Successful Assignment of guest_id {guest_ids} to room { room_no }. WiFi Password: {wifi_password}', 'success')
        return redirect(url_for('hospitality_staff_dashboard.check_in'))

    return render_template('assign_room.html', reservation_id=reservation_id, guest_id= guest_id, available_rooms=available_rooms)


# ROUTES FOR CHECK-OUT

@admin.route('/hospitality_staff_dashboard/check_out', methods=['GET', 'POST'])
@login_required
def check_out():

    # Get all the reservations that have check_out_date today and checked_out is False
    today = date.today()
    print(today) 

    reservation_today = Reservation.query.filter(Reservation.check_out_date == today, Reservation.checked_out == False).all()
    #Get room assignments to corrosponding reservations
    assignments = Assignment.query.filter(Assignment.reservation_id.in_([reservation.reservation_id for reservation in reservation_today])).all()
    #keep only those reservations where room no is not none
    assignments = [assignment for assignment in assignments if assignment.room_no is not None]
    reservation_today = [reservation for reservation in reservation_today if reservation.reservation_id in [assignment.reservation_id for assignment in assignments]]    

    # get room no from researvation_today from assignemnt table
    room_nos = [assignment.room_no for assignment in Assignment.query.filter(Assignment.reservation_id.in_([reservation.reservation_id for reservation in reservation_today])).all()]
    print(room_nos)

    # get the current_guests from the room_noss
    current_guests = current_guest.query.filter(current_guest.room_no.in_(room_nos)).all()

    #remove reservations where current_guest corrosponding to the room_no is not present


    form = enter_guest_idForm()
    if form.validate_on_submit():
        guest_id = form.guest_id.data
        return redirect(url_for('hospitality_staff_dashboard.check_out_billing', guest_id=guest_id))

    return render_template('check_out.html', form=form, current_guests=current_guests)

@admin.route('/hospitality_staff_dashboard/check_out_billing/<int:guest_id>', methods=['GET','POST'])
@login_required
def check_out_billing(guest_id):

    # Get all the bill ids associated with the guest_id from IncursBill table
    bill_ids = IncursBill.query.filter_by(guest_id=guest_id).all()
    print(bill_ids)
    # Get all the paid bills associated with the bill_ids
    unpaid_bills = Bill.query.filter(Bill.bill_id.in_([bill.bill_id for bill in bill_ids]), Bill.paid_status == '0').all()
    print(unpaid_bills)
    paid_bills = Bill.query.filter(Bill.bill_id.in_([bill.bill_id for bill in bill_ids]), Bill.paid_status == '1').all()
    print(paid_bills)

    total_paid_amount = sum(bill.amount for bill in paid_bills)
    total_unpaid_amount = sum(bill.amount for bill in unpaid_bills)

    if request.method == 'POST':
        payment_method = request.form['payment_method']
        for bill in unpaid_bills:
            bill.payment_method = payment_method
            bill.paid_status = True
        db.session.commit()
        flash('Payment completed! Click on the Check Out button to check out', 'success')
        
        unpaid_bills = Bill.query.filter(Bill.bill_id.in_([bill.bill_id for bill in bill_ids]), Bill.paid_status == '0').all()
        paid_bills = Bill.query.filter(Bill.bill_id.in_([bill.bill_id for bill in bill_ids]), Bill.paid_status == '1').all()
        total_paid_amount = sum(bill.amount for bill in paid_bills)
        total_unpaid_amount = sum(bill.amount for bill in unpaid_bills)

        return render_template('check_out_billing.html', paid_bills=paid_bills, unpaid_bills=unpaid_bills, guest_id=guest_id,
                                total_paid_amount=total_paid_amount, total_unpaid_amount=total_unpaid_amount)

    return render_template('check_out_billing.html', paid_bills=paid_bills, unpaid_bills=unpaid_bills, guest_id=guest_id,
                            total_paid_amount=total_paid_amount, total_unpaid_amount=total_unpaid_amount)

@admin.route('/hospitality_staff_dashboard/check_out_guest/<int:guest_id>', methods=['POST'])
@login_required
def check_out_guest(guest_id):
    

    current_guest_out = current_guest.query.get_or_404(guest_id)
    print(current_guest_out)
    room =current_guest_out.room_no
    assignment = Assignment.query.filter_by(room_no=room).first()
    reservation_id = assignment.reservation_id
    print(reservation_id)
    reservation = Reservation.query.get_or_404(reservation_id)
    reservation.checked_out = True

    past_guest = PastGuests(
        past_guest_id=guest_id,
        first_name=current_guest_out.first_name,
        last_name=current_guest_out.last_name,
        age=current_guest_out.age,
        street=current_guest_out.street,
        state=current_guest_out.state,
        pincode=current_guest_out.pincode,
        country=current_guest_out.country,
        phone_no=current_guest_out.phone_no,
        check_in_date=reservation.check_in_date,
        check_out_date=reservation.check_out_date,
        guest_category=current_guest_out.guest_category,
        visit_purpose=current_guest_out.visit_purpose,
        iitgn_id=current_guest_out.iitgn_id,
    )
#------------------
    # change the room check_out_cleaning to True
    room = Room.query.get_or_404(room)
    room.check_out_cleaning = True

    #create a maintenance request for the room to be cleaned
    highest_id = db.session.query(db.func.max(maintenance_request.request_id)).scalar()
    new_request = maintenance_request(
        request_id = highest_id + 1,
        description = f'CHECK-OUT: Cleaning in room {room.room_no}',
        date_created = datetime.datetime.now().date(),
        time_created = datetime.datetime.now().time(),
        status='open'
    )
    db.session.add(new_request)
    db.session.commit()

    # assign the maintenance_request_id and room_no to the RequiresMaintenance table
    requires_maintenance = RequiresMaintenance(
        request_id = highest_id + 1,
        room_no = room.room_no
    )
    db.session.add(requires_maintenance)

#------------------
    # add the past_guest to the past_guest table
    db.session.add(past_guest)
    # delete the current_guest from the current_guest table
    db.session.delete(current_guest_out)
    #delete the assignment from the assignment table
    db.session.delete(assignment)
    db.session.commit()
    flash('Guest checked out successfully!', 'success')
    return redirect(url_for('hospitality_staff_dashboard.check_out'))

# ROUTES FOR TRAVEL REQUESTS

@admin.route('/hospitality_staff_dashboard/travel_request', methods=['GET', 'POST'])
@login_required
def travel_requests():
    
    unassigned_travel_requests = travel_request.query.filter_by(driver_license=None).all()

    form = TravelRequestForm()
    if form.validate_on_submit():
        # Handle travel request form submission
       
        locked_table = select(travel_request).with_for_update()
        db.session.execute(locked_table)
       
        with db.session.begin_nested():
            highest_id = db.session.query(db.func.max(travel_request.travel_request_id)).scalar()
            if highest_id is None:
                highest_id = 0
            travel_request_new = travel_request(
                travel_request_id=highest_id + 1,
                number_of_travellers=form.number_of_travellers.data,
                date_of_travel=form.date_of_travel.data,
                pick_up_time=form.pick_up_time.data,
                destination=form.destination.data,
                travel_purpose=form.travel_purpose.data
            )


            db.session.add(travel_request_new)
        db.session.commit()
        flash('Travel request submitted successfully!', 'success')
        return redirect(url_for('hospitality_staff_dashboard.travel_requests'))
    return render_template('travel_request.html', form=form, unassigned_travel_requests=unassigned_travel_requests)


@admin.route('hospitality_staff_dashboard/travel_request_completed', methods=['GET'])
@login_required
def travel_request_completed():

    # Get all travel requests that all have pick_up_date less than today's date and driver_license is not None
    completed_travel_requests = travel_request.query.filter(travel_request.date_of_travel < datetime.datetime.now().date(), travel_request.driver_license.isnot(None)).all()
    return render_template('travel_request_completed.html', completed_travel_requests=completed_travel_requests)

@admin.route('/hospitality_staff_dashboard/driver_choose/<int:request_id>', methods=['GET', 'POST'])
@login_required
def driver_choose(request_id):

    request = travel_request.query.get_or_404(request_id)
    # Fetch all records of driver table
    driver_all = driver.query.all()

#------------------

    # Select drivers from driver_all who don't have any pending requests within +- 6 hours of the travel_request pick_up_time on the date_of _travel
    driver_available = []
    for drivers in driver_all: 
        pending_requests = travel_request.query.filter(travel_request.driver_license == drivers.driver_license, travel_request.date_of_travel >= request.date_of_travel).all()
        l = len(pending_requests)
        i = 0
        for pending_request in pending_requests:
            if pending_request.date_of_travel == request.date_of_travel and abs(request.pick_up_time.hour - request.pick_up_time.hour) < 6:
                print(pending_request)
                break
            i += 1
        if i == l:
            driver_available.append(drivers)
    print(driver_available)

#------------------
    pending_requests_by_driver_license = []

    # Get travel requests associated with a driver by filtering travel_requests on driver_license
    for drivers in driver_available:
        total_travel_requests = travel_request.query.filter_by(driver_license=drivers.driver_license).all()
        pending_travel_requests = [request for request in total_travel_requests if request.date_of_travel > datetime.datetime.now().date()]
        pending_requests_by_driver_license.append(len(pending_travel_requests))

    return render_template('travel_request_assignment.html', drivers=driver_available, pending_requests_by_driver_license=pending_requests_by_driver_license, request_id=request_id)

@admin.route('/hospitality_staff_dashboard/driver_assign/<int:travel_request_id>/<int:driver_license>', methods=['POST'])
@login_required
def driver_assign(travel_request_id, driver_license):

    travel_request_assign = travel_request.query.get_or_404(travel_request_id)
    travel_request_assign.driver_license = driver_license
    db.session.commit()
    flash(f'Maintenance request assigned successfully to driver {driver_license} !', 'success')
    return redirect(url_for('hospitality_staff_dashboard.travel_requests'))

# ROUTES FOR MAINTENANCE REQUESTS 

@admin.route('/hospitality_staff_dashboard/maintenance_requests', methods=['GET', 'POST'])
@login_required
def maintenance_request_view():

    #select maintainence requests where hospitality_staff_id is None
    open_maintenance_requests = maintenance_request.query.filter(maintenance_request.status == 'open', maintenance_request.housekeeping_staff_id.is_(None)).all()

#------------------
    #select open_maintenance_requests which belong to requires_maintenance table
    room_cleaning_requests = [request for request in open_maintenance_requests if request.request_id in [maintenance.request_id for maintenance in RequiresMaintenance.query.all()]]
   
    # other_requests = open_maintenance_requests - room_cleaning_requests
    other_requests = [request for request in open_maintenance_requests if request not in room_cleaning_requests]
#------------------

    form = MaintenanceRequestForm()

    if form.validate_on_submit():
        
        locked_table = select(maintenance_request).with_for_update()
        db.session.execute(locked_table)
        
        with db.session.begin_nested():
            highest_id = db.session.query(db.func.max(maintenance_request.request_id)).scalar()
            new_request = maintenance_request(
                request_id = highest_id + 1,
                description = form.description.data,
                date_created = datetime.datetime.now().date(),
                time_created = datetime.datetime.now().time(),
                status='open'
            )
            db.session.add(new_request)
        db.session.commit()
        flash('Maintenance request created successfully!', 'success')
        return redirect(url_for('hospitality_staff_dashboard.maintenance_request_view'))

    
    return render_template('maintenance_request.html', room_cleaning_requests=room_cleaning_requests, other_requests=other_requests,
                            form=form)

@admin.route('/hospitality_staff_dashboard/close_maintenance_request/<int:request_id>', methods=['POST'])
@login_required
def close_maintenance_request(request_id):

    maintenance_request_close = maintenance_request.query.get_or_404(request_id)
    maintenance_request_close.status = 'closed'
    db.session.commit()
    flash('Maintenance request closed successfully!', 'success')
    return redirect(url_for('hospitality_staff_dashboard.maintenance_request_view'))

@admin.route('/hospitality_staff_dashboard/maintenance_request_choose/<int:request_id>', methods=['GET', 'POST'])
@login_required
def maintenance_request_choose(request_id):

    # Fetch all records of housekeeping staff table
    housekeeping_staff_all = housekeeping_staff.query.all()
    open_requests_by_staff_id = []

    # Get maintenance requests associated with a housekeeping staff by filtering maintenance requests on housekeeping_staff_id
    for staff in housekeeping_staff_all:
        total_maintenance_requests = maintenance_request.query.filter_by(housekeeping_staff_id=staff.housekeeping_staff_id).all()
        open_maintenance_requests = [request for request in total_maintenance_requests if request.status == 'open']
        open_requests_by_staff_id.append(len(open_maintenance_requests))
    # count number of open requests assigned to each housekeeping staff

    return render_template('maintenance_request_assignment.html', housekeeping_staff=housekeeping_staff_all, open_requests_by_staff_id=open_requests_by_staff_id, request_id=request_id)
    
@admin.route('/hospitality_staff_dashboard/maintenance_request_assign/<int:request_id>/<int:staff_id>', methods=['POST'])
@login_required
def maintenance_request_assign(request_id, staff_id):

    maintenance_request_assign = maintenance_request.query.get_or_404(request_id)
    maintenance_request_assign.housekeeping_staff_id = staff_id
    db.session.commit()
    flash(f'Maintenance request assigned successfully to housekeeping staff {staff_id} !', 'success')
    return redirect(url_for('hospitality_staff_dashboard.maintenance_request_view'))

@admin.route('/hospitality_staff_dashboard/maintenance_requests_closed', methods=['GET'])
@login_required
def maintenance_request_closed():

    closed_maintenance_requests = maintenance_request.query.filter_by(status='closed').all()

    return render_template('maintenance_request_closed.html', closed_maintenance_requests= closed_maintenance_requests)

# ROUTES FOR RESERVATIONS

#-----------------
@admin.route('/hospitality_staff_dashboard/booking', methods=['GET', 'POST'])
@login_required
def booking():

#------------------
    # Get the reservation ids from reservation table where confirmed is 0
    reservations = Reservation.query.filter_by(confirmed=False).all()

    # update the Reservation.iitgn_id with Makes.iitgn_id corrosponding to the reservation_id
    for reservation in reservations:
        reservation.iitgn_id = Makes.query.filter_by(reservation_id=reservation.reservation_id).first().iitgn_id
#------------------

    form = BookingForm()
    if form.validate_on_submit():
        # Handle booking form submission
        
        locked_table = select(Reservation).with_for_update()
        db.session.execute(locked_table)
        
        with db.session.begin_nested():
            highest_id = db.session.query(db.func.max(Reservation.reservation_id)).scalar()
            if highest_id is None:
                highest_id = 0
            reservation = Reservation(
                reservation_id=highest_id + 1,
                number_of_people=form.number_of_people.data,
                check_in_date=form.check_in_date.data,
                check_out_date=form.check_out_date.data,
                room_type=form.room_type.data,
                specially_enabled_room_required=form.specially_enabled_room_required.data,
                comments=form.comments.data,
                email_id=form.email_id.data,
                iitgn_id=form.iitgn_id.data,
                checked_in=False,
                checked_out=False,
                confirmed=True
            )
            db.session.add(reservation)
        db.session.commit()
        flash(f'Reservation created successfully! Reservation ID: {reservation.reservation_id}', 'success')
        return redirect(url_for('hospitality_staff_dashboard.booking'))
    return render_template('booking.html', form=form, reservations=reservations)

#------------------
@admin.route('/hospitality_staff_dashboard/confirm_reservation/<int:reservation_id>', methods=['POST'])
@login_required
def confirm_reservation(reservation_id):
        reservation = Reservation.query.get_or_404(reservation_id)
        reservation.confirmed = True
        db.session.commit()
        flash('Reservation confirmed successfully!', 'success')
        return redirect(url_for('hospitality_staff_dashboard.booking'))
#------------------

@admin.route('/hospitality_staff_dashboard/viewreservations')
@login_required
def viewreservations():

    all_reservations = Reservation.query.all()

    return render_template('viewreservations.html', all_reservations=all_reservations)

# ROUTES FOR BILLS

@admin.route('/hospitality_staff_dashboard/billing', methods=['GET', 'POST'])
@login_required
def billing():
    bill = Bill.query.all()
    form = enter_guest_idForm()
    if form.validate_on_submit():
        # Handle create bill form submission
        guest_id = form.guest_id.data
        
        # Fetch all bill entries for the given guest_id
        incurs_bills = IncursBill.query.filter(IncursBill.guest_id == guest_id).all()
        
        if incurs_bills:
            paid_bills = Bill.query.filter(Bill.bill_id.in_([bill.bill_id for bill in incurs_bills]), Bill.paid_status == '1').all()
            unpaid_bills = Bill.query.filter(Bill.bill_id.in_([bill.bill_id for bill in incurs_bills]), Bill.paid_status == '0').all()
            total_unpaid_amount = sum(bill.amount for bill in unpaid_bills)
            total_paid_amount = sum(bill.amount for bill in paid_bills)
            flash(f'Bill generated successfully! for guest_id = {guest_id}', 'success')
            return render_template('bill_entries.html', paid_bills=paid_bills, total_unpaid_amount=total_unpaid_amount, total_paid_amount = total_paid_amount, guest_id=guest_id, unpaid_bills=unpaid_bills)
        else:
            flash('No bill found for the given guest ID!', 'danger')
            return redirect(url_for('hospitality_staff_dashboard.billing'))
    return render_template('billing.html', bill=bill, form=form)


@admin.route('/hospitality_staff_dashboard/create_bill', methods=['GET', 'POST'])
@login_required
def create_bill():
   
    form = billForm()


    paid_status=form.paid_status.data
    if paid_status == 1:
        paid_status = True
    else:  
        paid_status = False


    if form.validate_on_submit():
       
        locked_table = select(Bill).with_for_update()
        db.session.execute(locked_table)
       
        with db.session.begin_nested():
            highest_id = db.session.query(db.func.max(Bill.bill_id)).scalar()
            new_bill = Bill(
                bill_id = highest_id + 1,
                date_created = datetime.datetime.now().date(),
                time_created = datetime.datetime.now().time(),
                amount = form.amount.data,
                bill_type = form.bill_type.data,
                payment_method = form.payment_method.data,
                paid_status = paid_status,
                generated_by = form.generated_by.data,
                description = form.description.data
            )
            db.session.add(new_bill)
            db.session.flush()
            incurs_bill = IncursBill(
                guest_id = form.guest_id.data,
                bill_id = highest_id + 1
            )
            db.session.add(incurs_bill)
        db.session.commit()


        bill = Bill.query.filter(Bill.bill_id == highest_id + 1).first()
        print(bill)
        flash(f'Bill created successfully! Bill ID: {highest_id + 1}', 'success')
        return redirect(url_for('hospitality_staff_dashboard.create_bill'))
   
    else:
        print(form.errors)
   
    return render_template('create_bill.html', form=form)

@admin.route('/hospitality_staff_dashboard/pay_bill/<int:bill_id>', methods=['GET', 'POST'])    
@login_required
def pay_bill(bill_id):
    bill = Bill.query.get_or_404(bill_id)
    bill.paid_status = True
    db.session.commit()
    flash('Bill marked as paid!', 'success')
    return redirect(url_for('hospitality_staff_dashboard.billing'))


# ROUTES TO CHECK ROOM_AVAILABILITY BY DATE
#------------------
@admin.route('/hospitality_staff_dashboard/room_availability', methods=['GET', 'POST'])
@login_required
def room_availibility():
    if request.method == 'POST':
        date = request.form['date']
        return redirect(url_for('hospitality_staff_dashboard.room_availibility_by_date', date=date))
    return render_template('room_availability.html')

@admin.route('/hospitality_staff_dashboard/room_availability/<date>', methods=['GET'])
@login_required
def room_availibility_by_date(date):
    
    rooms = Room.query.all()

    # there are 6 types of rooms: double bed, twin bed, suite : each of them can be specially enabled or not
    # show number of room for each of the category available for booking on the given date
    # first count total of each type of room and then subtract the number of rooms booked on that date

    room_count= [0,0,0,0,0,0]
    for room in rooms:
        if room.room_type == 'double bed' and room.is_specially_enabled == False:
            room_count[0] += 1
        elif room.room_type == 'double bed' and room.is_specially_enabled == True:
            room_count[1] += 1
        elif room.room_type == 'twin bed' and room.is_specially_enabled == False:
            room_count[2] += 1
        elif room.room_type == 'twin bed' and room.is_specially_enabled == True:
            room_count[3] += 1
        elif room.room_type == 'suite' and room.is_specially_enabled == False:
            room_count[4] += 1
        elif room.room_type == 'suite' and room.is_specially_enabled == True:
            room_count[5] += 1

    print(room_count)
    available_rooms = room_count

    # get reservations where check_in_date <= date and check_out_date >= date

    reservations = Reservation.query.filter(Reservation.check_in_date <= date, Reservation.check_out_date > date).all()
    print(reservations)
    for reservation in reservations:
        print(reservation)
        print(reservation.room_type, reservation.specially_enabled_room_required)
        print()

        if reservation.room_type == 'Double Bed' and reservation.specially_enabled_room_required == False:
            available_rooms[0] -= 1
        elif reservation.room_type == 'Double Bed' and reservation.specially_enabled_room_required == True:
            available_rooms[1] -= 1
        elif reservation.room_type == 'Twin Bed' and reservation.specially_enabled_room_required == False:
            available_rooms[2] -= 1
        elif reservation.room_type == 'Twin Bed' and reservation.specially_enabled_room_required == True:
            available_rooms[3] -= 1
        elif reservation.room_type == 'Suite' and reservation.specially_enabled_room_required == False:
            available_rooms[4] -= 1
        elif reservation.room_type == 'Suite' and reservation.specially_enabled_room_required == True:
            available_rooms[5] -= 1

    print(available_rooms)
    return render_template('room_availability_by_date.html', available_rooms=available_rooms, date=date)

# ROUTES FOR FEEDBACK

@admin.route('/hospitality_staff_dashboard/feedback', methods=['GET', 'POST'])
def feedback():
    if request.method == 'POST':
       sorting_method = request.form['sort']
    else:
        sorting_method = 'date_desc'
    if sorting_method == 'date_desc':
        feedbacks = Feedback.query.order_by(Feedback.date.desc()).all()
    elif sorting_method == 'date_asc':
        feedbacks = Feedback.query.order_by(Feedback.date.asc()).all()
    elif sorting_method == 'rating_desc':
        feedbacks = Feedback.query.order_by(Feedback.star_rating.desc()).all()
    elif sorting_method == 'rating_asc':
        feedbacks = Feedback.query.order_by(Feedback.star_rating.asc()).all()
    return render_template('feedback.html', feedbacks=feedbacks)

