from flask import current_app as app
from flask import redirect, request, url_for, render_template
from flask_login import current_user
from flask_login.utils import login_required

import os
import requests
from dotenv import load_dotenv


from ..models.user_model import User
from ..models.spotify_access_token_model import SpotifyAccessToken
from .. import login_manager, db
from ..utils import spotify


load_dotenv()
CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
REDIRECT_URI = os.getenv("SPOTIFY_REDIRECT_URI")
BASE_URL = "https://accounts.spotify.com/authorize"


@app.route("/user/library")
def library():
    access_token = current_user.spotify_token.access_token

    playlists = spotify.get_playlists(access_token)

    return render_template("library.html", playlists=playlists)


@app.route("/user/library/playlist/<id>")
def playlist(id):
    access_token = current_user.spotify_token.access_token
    tracks = spotify.get_playlist(access_token, id)

    return tracks