from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from forms import BookingForm, CheckInForm, CheckOutForm, MaintenanceRequestForm, TravelRequestForm, LoginForm, RegistrationForm
from models import db, CurrentGuest, Room, HospitalityStaff, iitgn_member, Reservation, Bill, HousekeepingStaff, MaintenanceRequest, PastGuests, Feedback, TravelRequest, Driver, Booking, Assignment, RequiresMaintenance, ManagesMaintenance, ManagesReservation, IncursBill, Makes, GeneratesBill, InitiatedTravelRequest

app = Flask(__name__)

app.config['SECRET_KEY'] = 'abc'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqldb://root:<password>@localhost/guesthouse'

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
        user = iitgn_member.query.filter_by(email_id=form.email.data).first()
        print(user)
        if user and user.password == form.password.data:
            login_user(user)
        # Show a pop up message on the login page saying login successful
            flash('Login successful!', 'success')
        #redirect to the index page
            return redirect(url_for('index'))

        else:
            print(form.errors)
            
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

@app.route('/booking', methods=['GET', 'POST'])
@login_required
def booking():
    form = BookingForm()
    if form.validate_on_submit():
        # Handle booking form submission
        flash('Reservation created successfully!', 'success')
        return redirect(url_for('booking'))
    return render_template('booking.html', form=form)

@app.route('/check_in', methods=['GET', 'POST'])
@login_required
def check_in():
    form = CheckInForm()
    if form.validate_on_submit():
        # Handle check-in form submission
        flash('Guest checked in successfully!', 'success')
        return redirect(url_for('check_in'))
    return render_template('check_in.html', form=form)

@app.route('/check_out', methods=['GET', 'POST'])
@login_required
def check_out():
    form = CheckOutForm()
    if form.validate_on_submit():
        # Handle check-out form submission
        flash('Guest checked out successfully!', 'success')
        return redirect(url_for('check_out'))
    return render_template('check_out.html', form=form)

@app.route('/maintenance_request', methods=['GET', 'POST'])
@login_required
def maintenance_request():
    form = MaintenanceRequestForm()
    if form.validate_on_submit():
        # Handle maintenance request form submission
        flash('Maintenance request submitted successfully!', 'success')
        return redirect(url_for('maintenance_request'))
    return render_template('maintenance_request.html', form=form)

@app.route('/travel_request', methods=['GET', 'POST'])
@login_required
def travel_request():
    form = TravelRequestForm()
    if form.validate_on_submit():
        # Handle travel request form submission
        flash('Travel request submitted successfully!', 'success')
        return redirect(url_for('travel_request'))
    return render_template('travel_request.html', form=form)

@app.route('/home')
@login_required
def home():
    return render_template('home.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

