from flask import current_app as app
from flask import redirect, request, url_for, render_template, session, g

import os
from datetime import datetime, timedelta
import requests
from dotenv import load_dotenv

from ..utils import spotify
from ..utils.spotify import Spotify

from ..forms.create_playlist import CreatePlaylistForm


load_dotenv()
CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
REDIRECT_URI = os.getenv("SPOTIFY_REDIRECT_URI")
BASE_URL = "https://accounts.spotify.com/authorize"


@app.route("/user/library")
def library():
    playlists = []
    response = g.spotify.get_current_user_playlists(limit=50)
    for item in response["items"]:
        playlists.append(item)
    return render_template("library.html", playlists=playlists)


@app.route("/user/library/playlist/<id>", methods=["POST", "GET"])
def playlist(id):
    if request.method == "POST":
        session["seed_song"] = request.form["set_seed"]
        return redirect(url_for("playlist", id=id))
    elif request.method == "GET":
        sp = Spotify(session["access_token"])
        playlist = sp.get_playlist(id)

        tracks = []
        for item in playlist["tracks"]["items"]:
            tracks.append(item["track"])

        return render_template("playlist.html", tracks=tracks, playlist=playlist)


@app.route("/user/library/track/<id>")
def track(id):
    sp = Spotify(session["access_token"])

    track = sp.get_track(id)
    features = sp.get_track_audio_features(id)
    return render_template("track.html", track=track, features=features)


@app.route("/user/top/tracks/<term>", methods=["POST", "GET"])
def top_tracks(term):
    if request.method == "POST":
        session["seed_song"] = request.form["set_seed"]
        return redirect(url_for("top_tracks", term=term))
    elif request.method == "GET":
        sp = Spotify(session["access_token"])
        tracks = sp.get_top_tracks(limit=50, time_range=term)["items"]
        return render_template("playlist.html", tracks=tracks)


@app.route("/user/top/artists/<term>")
def top_artists(term):
    sp = Spotify(session["access_token"])
    artists = sp.get_top_artists(limit=50, time_range=term)["items"]
    return render_template("artists.html", artists=artists)


@app.route("/user/create-playlist", methods=["GET", "POST"])
def create_playlist():
    sp = Spotify(session["access_token"])
    form = CreatePlaylistForm()
    genres = sp.get_recommended_genres()["genres"]
    form.genres.choices = genres
    seed_song = "You haven't set your seed song, go to a playlist or top tracks to select a seed song"
    if session.get(seed_song):
        seed_song = session["seed_song"]
        track = seed_song[0]
        artist = seed_song[1]
    if form.validate_on_submit():
        # Create New Playlist with User Input Data
        if session.get("seed_song"):
            playlist_id = sp.create_playlist(
                sp.get_current_user()["id"],
                form.name.data,
                description=form.description.data,
            )["id"]

            # Get track recommendations from seeds
            seed = session["seed_song"].split()
            track_id = seed[0]
            artist_id = seed[1]

            recommendations = sp.get_recommendations(
                artist_id, form.genres.data, track_id, limit=50
            )["tracks"]

            # Convert Recommendations into list of uris
            tracks = []
            for track in recommendations:
                uri = track["uri"]
                tracks.append(uri)

            # Add tracks to the New Playlist
            sp.add_track_to_playlist(playlist_id, tracks)
            return redirect(url_for("playlist", id=playlist_id))
        else:
            return redirect(url_for("library"))
    return render_template("create_playlist.html", form=form)
