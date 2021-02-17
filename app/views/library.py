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
    total_playlists = g.spotify.get_current_user_playlists()["total"]
    offset = 0
    playlists = []
    while len(playlists) < total_playlists:
        items = g.spotify.get_current_user_playlists(offset=offset, limit=50)
        for item in items["items"]:
            playlists.append(item)
        offset = offset + 50
    return render_template("library.html", playlists=playlists)


@app.route("/user/library/playlist/<id>", methods=["POST", "GET"])
def playlist(id):
    if request.method == "POST":
        session["seed_song"] = request.form["set_seed"]
        return redirect(url_for("playlist", id=id))
    elif request.method == "GET":
        playlist = g.spotify.get_playlist(id)
        total_tracks = playlist["tracks"]["total"]
        offset = 0
        tracks = []
        while len(tracks) < total_tracks:
            items = g.spotify.get_playlist_items(id, offset=offset, limit=100)
            for item in items["items"]:
                tracks.append(item["track"])
            offset = offset + 100
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
    form = CreatePlaylistForm(meta={"csrf": False})
    genres = g.spotify.get_recommended_genres()["genres"]
    form.genres.choices = genres

    if session.get("seed_song"):
        seed_song = session["seed_song"].split(" ")
        track_id = seed_song[0]
        artist_id = seed_song[1]
        if form.validate_on_submit():
            num_tracks = form.num_tracks.data
            kwargs = {"limit": num_tracks}
            if form.advanced.data == True:
                # If both the column and row of the slider is active add the sliders value to kwargs
                if form.use_min.data == True:
                    if form.use_acousticness.data:
                        kwargs["min_acousticness"] = form.min_acousticness.data
                    if form.use_danceability.data:
                        kwargs["min_danceability"] = form.min_danceability.data
                    if form.use_liveness.data:
                        kwargs["min_liveness"] = form.min_liveness.data
                    if form.use_energy.data:
                        kwargs["min_energy"] = form.min_energy.data
                    if form.use_instrumentalness.data:
                        kwargs["min_instrumentalness"] = form.min_instrumentalness.data
                    if form.use_valence.data:
                        kwargs["min_valence"] = form.min_valence.data
                    if form.use_speechiness.data:
                        kwargs["min_speechiness"] = form.min_speechiness.data
                if form.use_max.data == True:
                    if form.use_acousticness.data:
                        kwargs["max_acousticness"] = form.max_acousticness.data
                    if form.use_danceability.data:
                        kwargs["max_danceability"] = form.max_danceability.data
                    if form.use_liveness.data:
                        kwargs["max_liveness"] = form.max_liveness.data
                    if form.use_energy.data:
                        kwargs["max_energy"] = form.max_energy.data
                    if form.use_instrumentalness:
                        kwargs["max_instrumentalness"] = form.max_instrumentalness.data
                    if form.use_valence.data:
                        kwargs["max_valence"] = form.max_valence.data
                    if form.use_speechiness.data:
                        kwargs["max_speechiness"] = form.max_speechiness.data
                if form.use_target.data == True:
                    if form.use_acousticness.data:
                        kwargs["target_acousticness"] = form.acousticness.data
                    if form.use_danceability.data:
                        kwargs["target_danceability"] = form.danceability.data
                    if form.use_liveness.data:
                        kwargs["target_liveness"] = form.liveness.data
                    if form.use_energy.data:
                        kwargs["target_energy"] = form.energy.data
                    if form.use_instrumentalness:
                        kwargs["target_instrumentalness"] = form.instrumentalness.data
                    if form.use_valence.data:
                        kwargs["target_valence"] = form.valence.data
                    if form.use_speechiness.data:
                        kwargs["target_speechiness"] = form.speechiness.data

            recommendations = g.spotify.get_recommendations(
                artist_id, form.genres.data, track_id, **kwargs
            )["tracks"]

            # Convert Recommendations into list of uris
            tracks = []
            for track in recommendations:
                uri = track["uri"]
                tracks.append(uri)

            # Create New Playlist with User Input Data
            playlist_id = g.spotify.create_playlist(
                g.spotify.get_current_user()["id"],
                form.name.data,
                description=form.description.data,
            )["id"]
            g.spotify.add_track_to_playlist(playlist_id, tracks)
            return redirect(url_for("playlist", id=playlist_id))
    else:
        return "No Seed Song"
    return render_template("create_playlist.html", form=form)
