from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField
from wtforms.validators import InputRequired, Length, ValidationError, NumberRange, EqualTo
from models import db, Users, Cameras

## These are Form objects from wtforms used to implement forms in webapp

## unique(name) factory of validators to check if username or camera alias is unique in database
def unique(name="name"):
    message = 'That %s already exists. Please choose a different one.' % (name)

    def _unique(form, field):
        existing = None
        if name == "alias":
            existing = Cameras.query.filter_by(alias=field.data).first()
        elif name == "username":
            existing = Users.query.filter_by(username=field.data).first()
        if existing:
            raise ValidationError(message)

    return _unique

## CameraForm() this is used to collect all information of the camera from the user
class CameraForm(FlaskForm):
    alias = StringField("alias", validators=[unique(name="alias")])
    uri = StringField("uri")
    width = IntegerField("width", validators=[NumberRange(min=10)])
    height = IntegerField("height", validators=[NumberRange(min=10)])
    
    submit = SubmitField('Add')
    
## EditCameraForm() this is used to collect all information of the camera from the user
class EditCameraForm(FlaskForm):
    alias = StringField("alias")
    uri = StringField("uri")
    width = IntegerField("width", validators=[NumberRange(min=10)])
    height = IntegerField("height", validators=[NumberRange(min=10)])
    
    submit = SubmitField('Change')

## LoginForm() this is used to collect ID from the user so specific item can be found
class LoginForm(FlaskForm):
    username = StringField("username", validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})
    password = PasswordField("password", validators=[InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "Password"})

    submit = SubmitField('Login')
    
## SearchForm() this is used to collect input from the user so specific camera or user can be found
class SearchForm(FlaskForm):
    search = StringField("search")
    
    submit = SubmitField('Search')

## ChangeSettingsForm() this is used to change user account info 
class ChangeSettingsForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=20), unique(name="username")], render_kw={"placeholder": "Username"})
    old_password = PasswordField('Old Password', validators=[InputRequired()], render_kw={"placeholder": "Old Password"})
    new_password = PasswordField('New Password', validators=[Length(min=8, max=20), EqualTo('confirm', message='Passwords must match')], render_kw={"placeholder": "New Password"})
    confirm  = PasswordField('Repeat Password', render_kw={"placeholder": "Repeat Password"})
    
    submit = SubmitField('Change')

## RegisterForm() this is used to collect input from the user so specific item can be found
class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=20), unique(name="username")], render_kw={"placeholder": "Username"})
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=20), EqualTo('confirm', message='Passwords must match')], render_kw={"placeholder": "Password"})
    confirm  = PasswordField('Repeat Password')
    
    submit = SubmitField('Register')