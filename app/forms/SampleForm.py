from Flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.fields.simple import SubmitField
from wtforms.validators import DataRequired, Length, ValidationError


class SampleForm(FlaskForm):
    sample_string = StringField("Email", validators=[DataRequired(), Length(2, 20)])
    submit = SubmitField("Submit")

    def validate_sample_string(self, sample_string):
        if sample_string != "Hello World":
            raise ValidationError("sample_string must be equal to: Hello World")
