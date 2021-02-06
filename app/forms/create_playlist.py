from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField
from wtforms.fields.simple import SubmitField
from wtforms.validators import DataRequired, Length, ValidationError


class CreatePlaylistForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    description = StringField("Description")
    public = BooleanField("Public")
    private = BooleanField("Private")
    collaborative = BooleanField("Collaborative")
    submit = SubmitField("Submit")