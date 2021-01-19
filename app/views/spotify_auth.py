from flask import current_app as app
from flask import render_template, redirect, request, url_for
import os
from dotenv import load_dotenv

from .. import login_manager

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
    code = request.args.get("code")
    print(code)
    return f"<h1>{code}</h1>"
