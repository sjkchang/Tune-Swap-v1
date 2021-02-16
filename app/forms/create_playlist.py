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
    danceability = DecimalRangeField("Danceability", default=0)
    valence = DecimalRangeField("Valence", default=0)
    acousticness = DecimalRangeField("Acousticness", default=0)
    instrumentalness = DecimalRangeField("Instrumentalness", default=0)
    liveness = DecimalRangeField("Valence", default=0)
    energy = DecimalRangeField("Energy", default=0)
    speechiness = DecimalRangeField("Speechiness", default=0)
    loudness = DecimalRangeField("Loudness", default=-60)

    submit = SubmitField("Submit")