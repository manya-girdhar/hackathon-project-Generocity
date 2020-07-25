from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError

class RegistrationForm(FlaskForm):
    firstname = StringField(
        "First Name",
        validators=[DataRequired(), Length(min=1, max=20)],
    )
    # 1st: name of field/label in html
    # 2nd: validation applied

    lastname = StringField(
        "Last Name",
        validators=[DataRequired(), Length(min=1, max=20)],
    )

    email = StringField(
        "Email",
        validators=[DataRequired(), Email()],
    )

    location = 

    password = PasswordField(
        "Password",
        validators=[DataRequired()],
    )

    confirm_password = PasswordField(
        "Confirm Password",
        validators=[DataRequired(), EqualTo("password")],
    )

    submit = SubmitField("Sign Up")

class LoginForm(FlaskForm):
    email = StringField(
        "Email",
        validators=[DataRequired(), Email()],
    )

    password = PasswordField(
        "Password",
        validators=[DataRequired()],
    )

    submit = SubmitField("Login")