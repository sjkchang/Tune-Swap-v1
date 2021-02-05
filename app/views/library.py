from flask import current_app as app
from flask import redirect, request, url_for, render_template, session

import os
import requests
from dotenv import load_dotenv

from ..utils import spotify
from ..utils.spotify import Spotify

load_dotenv()
CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
REDIRECT_URI = os.getenv("SPOTIFY_REDIRECT_URI")
BASE_URL = "https://accounts.spotify.com/authorize"

sp = None


@app.before_request
def refresh_token_create_spotify():
    if session.get("refresh_token"):
        URL = "https://accounts.spotify.com/api/token"

        body_params = {
            "grant_type": "refresh_token",
            "refresh_token": session["refresh_token"],
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
        }

        response = requests.post(URL, data=body_params).json()

        session["access_token"] = response
        session["access_token"]["refresh_token"] = session["refresh_token"]


@app.route("/user/library")
def library():
    sp = Spotify(session["access_token"])

    playlists = []
    response = sp.get_current_user_playlists(limit=50).json()
    for item in response["items"]:
        playlists.append(item)

    return render_template("library.html", playlists=playlists)


@app.route("/user/library/playlist/<id>")
def playlist(id):
    sp = Spotify(session["access_token"])

    tracks = []
    items = sp.get_playlist_items(id).json()["items"]
    for item in items:
        tracks.append(item["track"])

    # return str(tracks)
    return render_template("playlist.html", tracks=tracks)


@app.route("/user/library/track/<id>")
def track(id):
    sp = Spotify(session["access_token"])

    track = sp.get_track(id).json()
    return track


@app.route("/user/top/tracks/<term>")
def top_tracks(term):
    sp = Spotify(session["access_token"])
    tracks = sp.get_top_tracks(limit=50, time_range=term).json()["items"]
    return render_template("playlist.html", tracks=tracks)
