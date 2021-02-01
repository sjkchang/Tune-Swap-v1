from flask import current_app as app
from flask import redirect, request, url_for, render_template, session

import os
import requests
from dotenv import load_dotenv

from ..utils import spotify.Spotify


load_dotenv()
CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
REDIRECT_URI = os.getenv("SPOTIFY_REDIRECT_URI")
BASE_URL = "https://accounts.spotify.com/authorize"


@app.route("/user/library")
def library():
    access_token = session["access_token"]
    sp = spotify.Spotify(access_token)
    playlists = []
    response = sp.get_current_user_playlists(limit=50).json()
    for item in response["items"]:
        playlists.append(item)

    return render_template("library.html", playlists=playlists)


@app.route("/user/library/playlist/<id>")
def playlist(id):
    access_token = session["access_token"]
    sp = spotify.Spotify(access_token)
    tracks = []
    items = sp.get_playlist_items(id).json()["items"]
    for item in items:
        tracks.append(item["track"])

    return render_template("playlist.html", tracks=tracks)


@app.route("/user/library/track/<id>")
def track(id):
    access_token = session["access_token"]
    sp = spotify.Spotify(access_token)
    track = sp.get_track(id).json()
    return track


@app.route("/user/top/tracks/<term>")
def top_tracks(term):
    access_token = session["access_token"]
    sp = spotify.Spotify(access_token)
    tracks = sp.get_top_tracks(limit=50, time_range=term).json()["items"]

    return render_template("playlist.html", tracks=tracks)
