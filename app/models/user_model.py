from enum import unique
from sqlalchemy.sql.schema import PrimaryKeyConstraint
from .. import db, login_manager, bcrypt
from flask_login import UserMixin
from datetime import datetime


@login_manager.user_loader
def load_user(userId):
    return User.query.get(int(userId))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True, nullable=False)
    email = db.Column(db.String(64), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    active = db.Column(db.Boolean())
    date_created = db.Column(db.DateTime(), default=datetime.utcnow)

    spotify_code = db.Column(db.String(500))

    spotify_token_id = db.Column(db.Integer, db.ForeignKey("spotify_access_token.id"))
    spotify_token = db.relationship("SpotifyAccessToken", backref="User", uselist=False)

    def __str__(self):
        return f"Username: {self.username}"

    def __repr__(self):
        return f"<User {self.username!r}>"

    @classmethod
    def create(cls, username, email, password):
        password_hash = bcrypt.generate_password_hash(password)
        user = User(username=username, email=email, password_hash=password_hash)
        db.session.add(user)
        db.session.commit()

        return user

    def add_spotify_token(self, token):
        self.spotify_token = token
        db.session.add(self)
        db.session.commit()