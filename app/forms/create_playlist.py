from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    BooleanField,
    SelectField,
)
from wtforms.fields.html5 import DecimalRangeField
from wtforms.fields.simple import SubmitField
from wtforms.validators import DataRequired, Length, NumberRange, ValidationError


class CreatePlaylistForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    description = StringField("Description")
    num_tracks = DecimalRangeField("num_tracks")
    public = BooleanField("Public")
    private = BooleanField("Private")
    collaborative = BooleanField("Collaborative")
    genres = SelectField("genres", choices=[])
    advanced = BooleanField("advanced")

    use_target = BooleanField("Use Target")
    use_min = BooleanField("Use Min")
    use_max = BooleanField("Use Max")

    use_danceability = BooleanField("use_danceability")
    danceability = DecimalRangeField("Danceability", default=0)
    min_danceability = DecimalRangeField("Danceability", default=0)
    max_danceability = DecimalRangeField("Danceability", default=0)

    use_valence = BooleanField("use_valence")
    valence = DecimalRangeField("Valence", default=0)
    min_valence = DecimalRangeField("Valence", default=0)
    max_valence = DecimalRangeField("Valence", default=0)

    use_acousticness = BooleanField("use_acousticness")
    acousticness = DecimalRangeField("Acousticness", default=0)
    min_acousticness = DecimalRangeField("Acousticness", default=0)
    max_acousticness = DecimalRangeField("Acousticness", default=0)

    use_instrumentalness = BooleanField("use_instrumentalness")
    instrumentalness = DecimalRangeField("Instrumentalness", default=0)
    min_instrumentalness = DecimalRangeField("Instrumentalness", default=0)
    max_instrumentalness = DecimalRangeField("Instrumentalness", default=0)

    use_liveness = BooleanField("use_liveness")
    liveness = DecimalRangeField("Liveness", default=0)
    min_liveness = DecimalRangeField("Liveness", default=0)
    max_liveness = DecimalRangeField("Liveness", default=0)

    use_energy = BooleanField("use_energy")
    energy = DecimalRangeField("Energy", default=0)
    min_energy = DecimalRangeField("Energy", default=0)
    max_energy = DecimalRangeField("Energy", default=0)

    use_speechiness = BooleanField("use_speechiness")
    speechiness = DecimalRangeField("Speechiness", default=0)
    min_speechiness = DecimalRangeField("Speechiness", default=0)
    max_speechiness = DecimalRangeField("Speechiness", default=0)

    loudness = DecimalRangeField("Loudness", default=-60)

    submit = SubmitField("Submit")
