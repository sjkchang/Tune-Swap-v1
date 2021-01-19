from sqlalchemy.sql.schema import PrimaryKeyConstraint
from .. import db, login_manager
from flask_login import UserMixin


class User(db.Model, UserMixin):
    __id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), index=True, unique=True, nullable=False)
    active = db.Column(db.Boolean())
    date_created = db.Column(db.DateTime())

    def __str__(self):
        return f"Username: {self.username}"

    def __repr__(self):
        return f"<User {self.username!r}>"