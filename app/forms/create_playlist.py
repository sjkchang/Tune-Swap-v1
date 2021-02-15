from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    BooleanField,
    SelectField,
    SelectMultipleField,
    IntegerField,
)
from wtforms.fields.html5 import DecimalRangeField
from wtforms.fields.simple import SubmitField
from wtforms.validators import DataRequired, Length, NumberRange, ValidationError


class CreatePlaylistForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    description = StringField("Description")
    num_tracks = IntegerField("num_tracks")
    public = BooleanField("Public")
    private = BooleanField("Private")
    collaborative = BooleanField("Collaborative")
    genres = SelectField("genres", choices=[])
    submit = SubmitField("Submit")