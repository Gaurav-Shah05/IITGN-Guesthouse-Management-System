from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

class current_guest(db.Model):
    guest_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(20), nullable=False)
    last_name = db.Column(db.String(20), nullable=False)
    age = db.Column(db.Integer)
    street = db.Column(db.String(50))
    state = db.Column(db.String(15))
    pincode = db.Column(db.Integer)
    country = db.Column(db.String(20))
    phone_no = db.Column(db.String(20))
    guest_category = db.Column(db.String(10))
    visit_purpose = db.Column(db.String(100))
    iitgn_id = db.Column(db.Integer, db.ForeignKey('iitgn_member.iitgn_id'))
    room_no = db.Column(db.Integer, db.ForeignKey('room.room_no'))
    email_id = db.Column(db.String(100), nullable=True, unique=True)
    password = db.Column(db.String(20), nullable=True)
    first_login = db.Column(db.Boolean)
    role = 'current_guest'


    @property
    def is_active(self):
        # Replace with your logic for checking if the account is active
        return True
    
    def get_id(self):
        return str(self.guest_id)

class Room(db.Model):
    room_no = db.Column(db.Integer, primary_key=True)
    room_type = db.Column(db.String(10))
    is_specially_enabled = db.Column(db.Boolean)
    room_rent = db.Column(db.Integer, nullable=False)
    intercom_number = db.Column(db.String(10), unique=True)
#----------------
    check_out_cleaning = db.Column(db.Boolean)
#----------------


class hospitality_staff(db.Model):
    hospitality_staff_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(20), nullable=False)
    last_name = db.Column(db.String(20), nullable=False)
    age = db.Column(db.Integer)
    contact_no = db.Column(db.String(20), unique=True)
    street = db.Column(db.String(50))
    state = db.Column(db.String(15))
    staff_type = db.Column(db.String(50))
    salary = db.Column(db.Numeric)
    shift_time = db.Column(db.String(10))
    email_id = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(20), nullable=True)
    role = 'hospitality_staff'

    @property
    def is_active(self):
        # Replace with your logic for checking if the account is active
        return True
    
    def get_id(self):
        return str(self.hospitality_staff_id)
    
    

class iitgn_member(db.Model , UserMixin):
    iitgn_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(20), nullable=False)
    last_name = db.Column(db.String(20), nullable=False)
    member_type = db.Column(db.String(10))
    email_id = db.Column(db.String(100), unique=True)
    contact_no = db.Column(db.String(20), unique=True)
    password = db.Column(db.String(20), nullable=True)
    role = 'iitgn_member'

    @property
    def is_active(self):
        # Replace with your logic for checking if the account is active
        return True
    
    def get_id(self):
        return str(self.iitgn_id)


class Reservation(db.Model):
    reservation_id = db.Column(db.Integer, primary_key=True)
    number_of_people = db.Column(db.Integer)
    check_in_date = db.Column(db.Date, nullable=False)
    check_out_date = db.Column(db.Date, nullable=False)
    room_type = db.Column(db.String(10))
    specially_enabled_room_required = db.Column(db.Boolean)
    comments = db.Column(db.Text)
    email_id = db.Column(db.String(100), unique=True)
    checked_in = db.Column(db.Boolean)
    checked_out = db.Column(db.Boolean)
    iitgn_id = db.Column(db.Integer, db.ForeignKey('iitgn_member.iitgn_id'))
#----------------
    confirmed = db.Column(db.Boolean)
#----------------
class Bill(db.Model):
    bill_id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.Date)
    time_created = db.Column(db.Time)
    amount = db.Column(db.Numeric, nullable=False)
    bill_type = db.Column(db.String(20), nullable=False)
    payment_method = db.Column(db.String(15))
    paid_status = db.Column(db.Boolean)
    generated_by = db.Column(db.String(30))
    description = db.Column(db.Text)

class housekeeping_staff(db.Model):
    housekeeping_staff_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(20), nullable=False)
    last_name = db.Column(db.String(20), nullable=False)
    agency = db.Column(db.String(30))
    age = db.Column(db.Integer)
    contact_no = db.Column(db.String(20), unique=True)
    street = db.Column(db.String(50))
    pincode = db.Column(db.Integer)
    salary = db.Column(db.Numeric)
    shift_time = db.Column(db.String(10))
    email_id = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(20), nullable=True)

    @property
    def is_active(self):
        # Replace with your logic for checking if the account is active
        return True
    
    def get_id(self):
        return str(self.housekeeping_staff_id)



class maintenance_request(db.Model):
    request_id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.Text)
    status = db.Column(db.String(50))
    date_created = db.Column(db.Date, nullable=False)
    time_created = db.Column(db.Time, nullable=False)
    housekeeping_staff_id = db.Column(db.Integer, db.ForeignKey('housekeeping_staff.housekeeping_staff_id'), nullable=True)

class PastGuests(db.Model):
    past_guest_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(20), nullable=False)
    last_name = db.Column(db.String(20), nullable=False)
    age = db.Column(db.Integer)
    street = db.Column(db.String(50))
    state = db.Column(db.String(15))
    pincode = db.Column(db.Integer)
    country = db.Column(db.String(20))
    phone_no = db.Column(db.String(20))
    guest_category = db.Column(db.String(50))
    visit_purpose = db.Column(db.String(100))
    check_in_date = db.Column(db.Date, nullable=False)
    check_out_date = db.Column(db.Date, nullable=False)
    iitgn_id = db.Column(db.Integer, db.ForeignKey('iitgn_member.iitgn_id'), nullable=True)

class Feedback(db.Model):
    feedback_id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date)
    star_rating = db.Column(db.Integer)
    feedback = db.Column(db.Text)
    guest_id = db.Column(db.Integer, nullable=False)

class travel_request(db.Model):
    travel_request_id = db.Column(db.Integer, primary_key=True)
    number_of_travellers = db.Column(db.Integer)
    date_of_travel = db.Column(db.DateTime, nullable=False)
    pick_up_time = db.Column(db.Time, nullable=False)
    destination = db.Column(db.String(100), nullable=False)
    travel_purpose = db.Column(db.String(100), nullable=False)
    driver_license = db.Column(db.String(20), db.ForeignKey('driver.driver_license'), nullable=True)

class driver(db.Model):
    driver_license = db.Column(db.String(20), primary_key=True)
    first_name = db.Column(db.String(20), nullable=False)
    last_name = db.Column(db.String(20), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    agency = db.Column(db.String(100))
    car_description = db.Column(db.String(100))
    phone_number = db.Column(db.String(20), unique=True)
    experience = db.Column(db.Integer)
    email_id = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(20), nullable=True)

    @property
    def is_active(self):
        # Replace with your logic for checking if the account is active
        return True
    
    def get_id(self):
        return str(self.driver_license)

# Relationship tables

class Assignment(db.Model):
    room_no = db.Column(db.Integer, db.ForeignKey('room.room_no'), primary_key=True)
    reservation_id = db.Column(db.Integer, db.ForeignKey('reservation.reservation_id'))
    wifi_password = db.Column(db.String(20))

#----------------
class RequiresMaintenance(db.Model):
    request_id = db.Column(db.Integer, db.ForeignKey('maintenance_request.request_id'), primary_key=True)
    room_no = db.Column(db.Integer, db.ForeignKey('room.room_no'))
#----------------

class ManagesMaintenance(db.Model):
    request_id = db.Column(db.Integer, db.ForeignKey('maintenance_request.request_id'), primary_key=True)
    hospitality_staff_id = db.Column(db.Integer, db.ForeignKey('hospitality_staff.hospitality_staff_id'))

class ManagesReservation(db.Model):
    reservation_id = db.Column(db.Integer, db.ForeignKey('reservation.reservation_id'), primary_key=True)
    hospitality_staff_id = db.Column(db.Integer, db.ForeignKey('hospitality_staff.hospitality_staff_id'))
    comments = db.Column(db.Text, nullable=False)

class IncursBill(db.Model):
    guest_id = db.Column(db.Integer, db.ForeignKey('current_guest.guest_id'), primary_key=True)
    bill_id = db.Column(db.Integer, db.ForeignKey('bill.bill_id'), primary_key=True)

class Makes(db.Model):
    reservation_id = db.Column(db.Integer, db.ForeignKey('reservation.reservation_id'), primary_key=True)
    iitgn_id = db.Column(db.Integer, db.ForeignKey('iitgn_member.iitgn_id'))


class GeneratesBill(db.Model):
    bill_id = db.Column(db.Integer, db.ForeignKey('bill.bill_id'), primary_key=True)
    hospitality_staff_id = db.Column(db.Integer, db.ForeignKey('hospitality_staff.hospitality_staff_id'))
    comments = db.Column(db.Text, nullable=False)

class InitiatedTravelRequest(db.Model):
    travel_request_id = db.Column(db.Integer, db.ForeignKey('travel_request.travel_request_id'), primary_key=True)
    guest_id = db.Column(db.Integer, db.ForeignKey('current_guest.guest_id'))
