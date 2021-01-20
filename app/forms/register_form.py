from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from ..models.user_model import User


class RegistrationForm(FlaskForm):
    """Form used to gather user input data for User registration
    Raises:
        ValidationError: Raises a validation error if the username or email
        are already assigned to another user
    """

    username = StringField(
        "Username", validators=[DataRequired(), Length(min=2, max=20)]
    )
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=8)])
    confirmPassword = PasswordField(
        "Confirm Password",
        validators=[DataRequired(), Length(min=8), EqualTo("password")],
    )
    submit = SubmitField("Sign Up")
