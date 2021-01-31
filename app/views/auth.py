from flask import current_app as app
from flask import redirect, request, url_for, session

import os
import requests
from dotenv import load_dotenv

from ..utils import spotify


load_dotenv()
CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
REDIRECT_URI = os.getenv("SPOTIFY_REDIRECT_URI")
BASE_URL = "https://accounts.spotify.com/authorize"

### AUTHENTICATION
#######################################################
@app.route("/spotify/auth", methods=["GET", "POST"])
def authenticate():
    URL = (
        BASE_URL
        + f"?client_id={CLIENT_ID}"
        + "&response_type=code"
        + f"&redirect_uri={REDIRECT_URI}"
        + "&scope=user-read-private%20user-read-email%20user-library-read%20user-library-modify%20playlist-modify-public%20playlist-modify-private%20playlist-read-private%20user-read-recently-played%20user-top-read%20user-read-playback-position"
    )
    return redirect(URL)


@app.route("/spotify/auth/callback")
def callback():
    session["code"] = request.args.get("code")

    URL = "https://accounts.spotify.com/api/token"

    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
    }

    body_params = {
        "grant_type": "authorization_code",
        "code": session["code"],
        "redirect_uri": "http://127.0.0.1:5000/spotify/auth/callback",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
    }
    data = requests.post(URL, data=body_params).json()

    session["access_token"] = data
    session["refresh_token"] = data["refresh_token"]

    return redirect(url_for("home"))


@app.route("/spotify/auth/refresh")
def refresh():
    URL = "https://accounts.spotify.com/api/token"

    body_params = {
        "grant_type": "refresh_token",
        "refresh_token": session["refresh_token"],
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
    }

    response = requests.post(URL, data=body_params)
    response = response.json()
    print(response)

    session["access_token"] = response

    return redirect(url_for("home"))


### API Calls
########################################################################