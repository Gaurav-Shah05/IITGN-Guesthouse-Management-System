from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, DateField, BooleanField, TextAreaField, PasswordField, SelectField, SubmitField
from wtforms.validators import DataRequired, Email, Length, ValidationError

class BookingForm(FlaskForm):
    number_of_people = IntegerField('Number of People', validators=[DataRequired()])
    check_in_date = DateField('Check-in Date', validators=[DataRequired()])
    check_out_date = DateField('Check-out Date', validators=[DataRequired()])
    room_type = SelectField('Room Type', choices=[('single', 'Single'), ('double', 'Double'), ('suite', 'Suite')], validators=[DataRequired()])
    specially_enabled_room_required = BooleanField('Specially Enabled Room Required')
    comments = TextAreaField('Comments')

class CheckInForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    age = IntegerField('Age', validators=[DataRequired()])
    street = StringField('Street', validators=[DataRequired()])
    state = StringField('State', validators=[DataRequired()])
    pincode = IntegerField('Pincode', validators=[DataRequired()])
    country = StringField('Country', validators=[DataRequired()])
    phone_no = StringField('Phone Number', validators=[DataRequired()])
    guest_category = SelectField('Guest Category', choices=[('student', 'Student'), ('faculty', 'Faculty'), ('other', 'Other')], validators=[DataRequired()])
    visit_purpose = TextAreaField('Visit Purpose', validators=[DataRequired()])
    iitgn_id = IntegerField('IITGN ID', validators=[])

class CheckOutForm(FlaskForm):
    guest_id = IntegerField('Guest ID', validators=[DataRequired()])

class MaintenanceRequestForm(FlaskForm):
    description = TextAreaField('Description', validators=[DataRequired()])
    room_no = IntegerField('Room Number', validators=[DataRequired()])

class TravelRequestForm(FlaskForm):
    number_of_travellers = IntegerField('Number of Travellers', validators=[DataRequired()])
    date_of_travel = DateField('Date of Travel', validators=[DataRequired()])
    pick_up_time = StringField('Pick-up Time', validators=[DataRequired()])
    destination = StringField('Destination', validators=[DataRequired()])
    travel_purpose = TextAreaField('Travel Purpose', validators=[DataRequired()])

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class RegistrationForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), Length(min=6)])
    submit = SubmitField('Register')

    def validate_confirm_password(self, field):
        if field.data != self.password.data:
            raise ValidationError('Passwords do not match')