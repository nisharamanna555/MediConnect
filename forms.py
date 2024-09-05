from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FileField, SelectField, DateField, IntegerField
from wtforms.validators import DataRequired, Email, EqualTo, InputRequired

class RegisterForm(FlaskForm):
    user = SelectField(label='',
                       choices=[('patient', 'Patient'),('pharmacy', 'Pharmacy'),('physician','Physician')],
                       validators=[DataRequired()])

class LoginForm(FlaskForm):
    user = SelectField(label='',
                       choices=[('patient', 'Patient'),('pharmacy', 'Pharmacy'),('physician','Physician')],
                       validators=[DataRequired()])
    username = StringField(label='Username', validators=[DataRequired()])
    password = PasswordField(label='Password', validators=[DataRequired()])
    submit = SubmitField(label='Login')

class ResetRequestForm(FlaskForm):
    user = SelectField(label='Select the type of account you have:',
                       choices=[('patient', 'Patient'),('pharmacy', 'Pharmacy'),('physician','Physician')],
                       validators=[DataRequired()])
    email = StringField(label='Email', validators=[DataRequired(), Email()])
    submit = SubmitField(label='Reset Password', validators=[DataRequired()])

class ResetPasswordForm(FlaskForm):
    password = PasswordField(label='Password', validators=[DataRequired()])
    confirm_password = PasswordField(label='Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField(label='Change Password', validators=[DataRequired()])

class UploadForm(FlaskForm):
    file = FileField(label='File', validators=[InputRequired()])
    submit = SubmitField(label='Upload Insurance Card', validators=[DataRequired()])

class EditButtonForm(FlaskForm):
    submit = SubmitField(label='Edit Your Profile', validators=[DataRequired()])

class EditInfoForm(FlaskForm):
    first_name = StringField(label='', validators=[DataRequired()])
    last_name = StringField(label='', validators=[DataRequired()])
    d_o_b = DateField(label='', format='%Y-%m-%d', validators=[DataRequired()])
    sex = StringField(label='', validators=[DataRequired()])
    phone_number = StringField(label='', validators=[DataRequired()])
    emergency_cont = StringField(label='', validators=[DataRequired()])
    building_num = IntegerField(label='', validators=[DataRequired()])
    apt_num = StringField(label='')
    street_name = StringField(label='', validators=[DataRequired()])
    city = StringField(label='', validators=[DataRequired()])
    state = StringField(label='', validators=[DataRequired()])
    zip_code = IntegerField(label='', validators=[DataRequired()])
    submit = SubmitField(label='Submit Changes', validators=[DataRequired()])

class BackForm(FlaskForm):
    back = SubmitField(label='Back', validators=[DataRequired()])