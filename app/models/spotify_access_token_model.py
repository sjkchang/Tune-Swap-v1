from sqlalchemy.sql.schema import ForeignKey, PrimaryKeyConstraint
from .. import db
from flask_login import UserMixin
from datetime import datetime


class SpotifyAccessToken(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    access_token = db.Column(db.String(128), nullable=False)
    token_type = db.Column(db.String(128), nullable=False)
    scope = db.Column(db.String(128), nullable=False)
    expires_in = db.Column(db.Integer, nullable=False)
    refresh_token = db.Column(db.String(128), nullable=False)

    def __str__(self):
        return f"Access_token: {self.access_token}, scope: {self.scope}, refresh_token: {self.refresh_token}"

    def __repr__(self):
        return f"Access_token: {self.access_token}, scope: {self.scope}, refresh_token: {self.refresh_token}"

    @classmethod
    def create(cls, access_token, token_type, scope, expires_in, refresh_token):
        token = SpotifyAccessToken(
            access_token=access_token,
            token_type=token_type,
            scope=scope,
            expires_in=expires_in,
            refresh_token=refresh_token,
        )
        db.session.add(token)
        db.session.commit()

        return token