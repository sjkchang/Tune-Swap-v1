from flask import current_app as app
from flask import redirect, request, url_for, session, g

import os
import requests
from datetime import datetime, timedelta
from dotenv import load_dotenv

from ..utils.spotify import Spotify

load_dotenv()
CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
REDIRECT_URI = os.getenv("SPOTIFY_REDIRECT_URI")
BASE_URL = "https://accounts.spotify.com/authorize"


@app.before_request
def refresh_token_create_spotify():
    refresh_expired_token()
    setup_spotify()
    print("Poopy")


def refresh_expired_token():
    if session.get("refresh_token") and (session["expires_at"] <= datetime.now()):
        URL = "https://accounts.spotify.com/api/token"

        body_params = {
            "grant_type": "refresh_token",
            "refresh_token": session["refresh_token"],
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
        }

        response = requests.post(URL, data=body_params)

        session["access_token"] = response.json()
        session["access_token"]["refresh_token"] = session["refresh_token"]
        session["expires_at"] = datetime.now() + timedelta(hours=1)


def setup_spotify():
    if session.get("access_token"):
        g.spotify = Spotify(session["access_token"])