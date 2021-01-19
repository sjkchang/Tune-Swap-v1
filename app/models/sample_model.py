from sqlalchemy.sql.schema import PrimaryKeyConstraint
from .. import db


class SampleModel(db.Model):
    __id = db.Column(db.Integer, primary_key=True)
    SampleString = db.Column(db.String(20), index=True, unique=True, nullable=False)