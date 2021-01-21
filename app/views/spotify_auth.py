from flask import current_app as app
from flask import render_template, redirect, request, url_for
from flask_login import current_user

import os
import requests
import urllib
import base64
from dotenv import load_dotenv

from ..models.user_model import User
from ..models.spotify_access_token_model import SpotifyAccessToken
from .. import login_manager, db

load_dotenv()
CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
REDIRECT_URI = os.getenv("SPOTIFY_REDIRECT_URI")
BASE_URL = "https://accounts.spotify.com/authorize"


@app.route("/spotify/auth", methods=["GET", "POST"])
def authenticate():
    URL = (
        BASE_URL
        + f"?client_id={CLIENT_ID}"
        + "&response_type=code"
        + f"&redirect_uri={REDIRECT_URI}"
        + "&scope=user-read-private"
    )
    print(URL)
    return redirect(URL)


@app.route("/spotify/auth/callback")
def callback():
    current_user.spotify_code = request.args.get("code")
    code = request.args.get("code")
    db.session.commit()
    print("running")
    return redirect(url_for("home"))


@app.route("/spotify/auth/refresh")
def requestTokens():
    URL = "https://accounts.spotify.com/api/token"

    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
    }

    body_params = {
        "grant_type": "authorization_code",
        "code": current_user.spotify_code,
        "redirect_uri": "http://127.0.0.1:5000/spotify/auth/callback",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
    }
    response = requests.post(URL, data=body_params)
    data = response.json()
    token = SpotifyAccessToken.create(
        data["access_token"],
        data["token_type"],
        data["scope"],
        data["expires_in"],
        data["refresh_token"],
    )
    return f"<h1>{str(data)}</h1>"
