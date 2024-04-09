from flask import Flask, render_template, request, redirect, url_for, flash, app
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from forms import BookingForm, CheckInForm, CheckOutForm, MaintenanceRequestForm, TravelRequestForm, LoginForm, RegistrationForm
from models import db, current_guest, Room, hospitality_staff, iitgn_member, travel_request, Reservation, Bill, housekeeping_staff, maintenance_request, PastGuests, Feedback, driver, Assignment, RequiresMaintenance, ManagesMaintenance, ManagesReservation, IncursBill, Makes, GeneratesBill, InitiatedTravelRequest
from datetime import datetime
from admin import admin
from member import member
from guest import guest
from staff import staff
from Driver import Driver

app = Flask(__name__)
app.register_blueprint(admin, url_prefix='/')
app.register_blueprint(member, url_prefix='/')
app.register_blueprint(guest, url_prefix='/')
app.register_blueprint(staff, url_prefix='/')
app.register_blueprint(Driver, url_prefix='/')

app.config['SECRET_KEY'] = 'abc'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqldb://root:asterix@localhost/guesthouse_db'

db.init_app(app)

login_manager = LoginManager(app)


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(iitgn_member, int(user_id))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        print(form.email.data)
        user = hospitality_staff.query.filter_by(email_id=form.email.data).first()
        if user is not None and user.password == form.password.data:
            login_user(user)
            current_user.role = 'hospitality_staff'
            flash('Login successful!', 'success')
            return redirect(url_for('hospitality_staff_dashboard'))
        
        user = current_guest.query.filter_by(email_id=form.email.data).first()
        if user is not None and user.password == form.password.data:
            login_user(user)
            current_user.role = 'current_guest'
            flash('Login successful!', 'success')
            return redirect(url_for('current_guest_dashboard'))
        
        user = iitgn_member.query.filter_by(email_id=form.email.data).first()
        if user is not None and user.password == form.password.data:
            login_user(user)
            current_user.role = 'iitgn_member'
            flash('Login successful!', 'success')
            return redirect(url_for('iitgn_member_dashboard'))
        
        user = housekeeping_staff.query.filter_by(email_id=form.email.data).first()
        if user is not None and user.password == form.password.data:
            login_user(user)
            flash('Login successful!', 'success')
            return redirect(url_for('housekeeping_staff_dashboard'))

        
        user = driver.query.filter_by(email_id=form.email.data).first()
        if user is not None and user.password == form.password.data:
            login_user(user)
            flash('Login successful!', 'success')
            return redirect(url_for('driver_dashboard'))
        
        
        flash('Invalid Credentials', 'danger')
        return redirect(url_for('login'))
    
    return render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = iitgn_member(
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            email_id=form.email.data,
            password=form.password.data
        )
        db.session.add(user)
        db.session.commit()
        flash('Registration successful!', 'success')
        return redirect(url_for('login'))
    else:
        print(form.errors)
    return render_template('register.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('index'))

# Routes for different dashboards

@app.route('/current_guest_dashboard')
@login_required
def current_guest_dashboard():

    id = current_user.get_id()  
    print(id)  
    current_guest_pass = current_guest.query.filter_by(guest_id = id).first()
    print(current_guest_pass)
    print(current_guest.query.filter_by(guest_id = 4).all())
    print(current_guest_pass.room_no)
    first_login = current_guest_pass.first_login;
    assignment = Assignment.query.filter_by(room_no = current_guest_pass.room_no).first()
    print(assignment)

    initiated_travel_request = InitiatedTravelRequest.query.filter_by(guest_id = id).all()
    unassigned_travel_Request = []
    assigned_travel_Request = []
    
    for initiated_travel_request in initiated_travel_request:
        
        unassigned_travel_Request += travel_request.query.filter(travel_request.date_of_travel >= datetime.today().date(),
            travel_request.travel_request_id == initiated_travel_request.travel_request_id, travel_request.driver_license == None).all()
        assigned_travel_Request += travel_request.query.filter(travel_request.date_of_travel >= datetime.today().date(),
            travel_request.travel_request_id == initiated_travel_request.travel_request_id, travel_request.driver_license != None).all()

    if first_login == False:
        return render_template('current_guest_dashboard.html', currentguest=current_guest_pass, assignment = assignment, unassigned_travel_Request=unassigned_travel_Request, assigned_travel_Request=assigned_travel_Request)
    else:
        return redirect(url_for('current_guest_dashboard.first_login'))


    #return render_template('current_guest_dashboard.html')

@app.route('/hospitality_staff_dashboard')
@login_required
def hospitality_staff_dashboard():

    currentguest = current_guest.query.order_by(current_guest.room_no).all()
    
    assign_open_main_requests = maintenance_request.query.filter(maintenance_request.status == 'open', maintenance_request.housekeeping_staff_id.isnot(None)).all()
    
    return render_template('hospitality_staff_dashboard.html',currentguest=currentguest, assign_open_main_requests=assign_open_main_requests)

@app.route('/iitgn_member_dashboard')
@login_required
def iitgn_member_dashboard():

    makes = Makes.query.filter_by(iitgn_id = current_user.get_id()).first()
    reservation_id = Reservation.query.filter_by(reservation_id = makes.reservation_id).all()
    # print(reservation_id.reservation_id)

    
    # reservation = Reservation.query.filter_by(reservation_id = reservation_id.reservation_id).all()
    # print(reservation)
    
    #iterate over all reservations and get the details of each reservation
    reservations =[]
    for i in reservation_id:
        reservations.append(Reservation.query.filter_by(reservation_id = i.reservation_id).first())
    return render_template('iitgn_member_dashboard.html', member_reservations=reservations)

@app.route('/housekeeping_staff_dashboard')
@login_required
def housekeeping_staff_dashboard():
    return render_template('housekeeping_staff_dashboard.html')

@app.route('/driver_dashboard')
@login_required
def driver_dashboard():
    return render_template('driver_dashboard.html')










if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

