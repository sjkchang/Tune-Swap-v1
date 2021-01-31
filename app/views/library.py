from flask import current_app as app
from flask import redirect, request, url_for, render_template, session

import os
import requests
from dotenv import load_dotenv

from ..utils import spotify


load_dotenv()
CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
REDIRECT_URI = os.getenv("SPOTIFY_REDIRECT_URI")
BASE_URL = "https://accounts.spotify.com/authorize"


@app.route("/user/library")
def library():
    access_token = session["access_token"]["access_token"]

    playlists = spotify.get_playlists_simplified(access_token)

    return render_template("library.html", playlists=playlists)


@app.route("/user/library/playlist/<id>")
def playlist(id):
    access_token = session["access_token"]["access_token"]
    tracks = spotify.get_playlist(access_token, id)["items"]
    return render_template("playlist.html", tracks=tracks)


@app.route("/user/library/track/<id>")
def track(id):
    access_token = session["access_token"]["access_token"]
    track = spotify.get_track(access_token, id)
    return track


@app.route("/user/top/tracks/<term>")
def top_tracks(term):
    access_token = session["access_token"]["access_token"]

    tracks = spotify.get_top_tracks(access_token, term)

    return render_template("playlist.html", tracks=tracks)