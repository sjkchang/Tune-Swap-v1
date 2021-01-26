from flask import current_app as app
from flask import redirect, request, url_for
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

### AUTHENTICATION
#######################################################
@app.route("/spotify/auth", methods=["GET", "POST"])
def authenticate():
    URL = (
        BASE_URL
        + f"?client_id={CLIENT_ID}"
        + "&response_type=code"
        + f"&redirect_uri={REDIRECT_URI}"
        + "&scope=user-read-private%20user-read-email%20user-library-read%20user-library-modify%20playlist-modify-public%20playlist-modify-private%20playlist-read-private"
    )
    print(URL)
    return redirect(URL)


@app.route("/spotify/auth/callback")
def callback():
    current_user.spotify_code = request.args.get("code")
    code = request.args.get("code")
    db.session.commit()
    print("running")
    return redirect(url_for("refresh"))


@app.route("/spotify/auth/refresh")
def refresh():
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
    print(data)
    token = SpotifyAccessToken.create(
        data["access_token"],
        data["token_type"],
        data["scope"],
        data["expires_in"],
        data["refresh_token"],
    )
    current_user.add_spotify_token(token)

    return redirect(url_for("home"))


### API Calls
########################################################################


@login_required
@app.route("/test", methods=["GET", "POST"])
def test():
    token = current_user.spotify_token

    access_token = token.access_token
    user = spotify.getCurrentUser(access_token)
    playlists = spotify.get_playlists(access_token, 50)
    track = spotify.get_uri_for_track(
        access_token, "This is Home", "Cavetown", "This is Home"
    )
    # new_playlist = spotify.create_playlist(
    #  access_token, "Api test playlist", "Test", False
    # )
    add_song = spotify.add_track_to_playlist(
        access_token, "375vOdUrkRS1nspEU0SDk7", "spotify:track:7s8VgA8OjvwBUuigKzEGBx"
    )
    return f"""
            <h1>User</h1>
            <p>{user}</p>
            <h1>Playlists</h1>
            <p>{playlists}</p>
            <h1>Meet Virginia</h1>
            <p>{track}</p>
            <h1>New Playlist</h1>
            <p></p>
            <h1>new_track</h1>
            <p>{add_song}</p>
            <h1></h1>
            <p></p>
        """