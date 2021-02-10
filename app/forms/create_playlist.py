from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SelectField, SelectMultipleField
from wtforms.fields.simple import SubmitField
from wtforms.validators import DataRequired, Length, ValidationError


class CreatePlaylistForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    description = StringField("Description")
    public = BooleanField("Public")
    private = BooleanField("Private")
    collaborative = BooleanField("Collaborative")
    genres = SelectField("genres", choices=[])
    submit = SubmitField("Submit")