from flask_wtf import FlaskForm
from wtforms import EmailField, PasswordField, SubmitField, StringField, BooleanField
from wtforms.validators import DataRequired, ValidationError, EqualTo, Length
from  flask_wtf.file import FileField
from app.models import User






class reset_requestform(FlaskForm):
    email = EmailField('Email', validators=[DataRequired()])
    Submit= SubmitField('Request Reset')

    def validate_Email(self, Email):
        user= User.query.filter_by(email= Email.data).first()
        if user is None:
            raise ValidationError('This Email does not exists, you must register first.')

class reset_passwordform(FlaskForm):
    password1 = PasswordField('Password', validators=[EqualTo( 'password2' , 'Password does not match'), Length(8,10, 'Password must be between 8 & 10 characters'), DataRequired()])
    password2 = PasswordField('Confirm Password', validators=[DataRequired()])
    Submit= SubmitField('Reset Password')



class profile_editform(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired()])
    location = StringField('Location', validators=[DataRequired()])
    About_me =StringField('Tell us a bit about you', validators=[DataRequired()])
    profilepic =FileField('upload image')
    Submit= SubmitField('update profile')

    def validate_Email(self, Email):
        user= User.query.filter_by(email= Email.data).first()
        if user:
            raise ValidationError('This Email Already Exists')



class Registration_form(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired()])
    password1 = PasswordField('Password', validators=[EqualTo( 'password2' , 'Password does not match'), Length(8,10, 'Password must be between 8 & 10 characters'), DataRequired()])
    password2 = PasswordField('Confirm Password', validators=[DataRequired()])
    Submit= SubmitField('Register')
    
    def validate_Email(self, Email):
        user= User.query.filter_by(email= Email.data).first()
        if user:
            raise ValidationError('This Email Already Exists')


class Login_form(FlaskForm):
    email = EmailField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    Remember = BooleanField('Keep me logged in')
    Submit= SubmitField('Login')