from flask import current_app as app
from flask import render_template, session, request, redirect
from flask.helpers import url_for

from ..utils.spotify import Spotify
import json
import requests


@app.route("/", methods=["GET", "POST"])
def landing():
    if request.method == "POST":
        return redirect(url_for("authenticate"))
    else:
        return render_template("landing.html")


@app.route("/home")
def home():
    code = "N/a"
    access_token = "n/a"
    me = "n/a"
    seed_song = "n/a"
    if session.get("code"):
        code = session["code"]
    if session.get("access_token"):
        access_token = session["access_token"]
        sp = Spotify(access_token)

        me = sp.get_current_user()
        me = me
    if session.get("seed_song"):
        seed_song = session["seed_song"]

    return render_template(
        "home.html", code=code, access_token=access_token, me=me, seed_song=seed_song
    )


@app.route("/account")
def account():
    sp = Spotify(session["access_token"])

    current_user = sp.get_current_user()
    return render_template("account.html", current_user=current_user)
