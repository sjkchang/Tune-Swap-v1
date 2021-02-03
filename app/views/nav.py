from flask import current_app as app
from flask import render_template, session

from ..utils.spotify import Spotify
import json
import requests


@app.route("/landing")
def landing():
    return render_template("landing.html")


@app.route("/")
def home():
    code = "N/a"
    access_token = "n/a"
    me = "n/a"
    if session.get("code"):
        code = session["code"]
    if session.get("access_token"):
        access_token = session["access_token"]
        sp = Spotify(access_token)

        me = sp.get_current_user()
        me = me.json()

    return render_template("home.html", code=code, access_token=access_token, me=me)


@app.route("/account")
def account():
    sp = Spotify(session["access_token"])

    current_user = sp.get_current_user().json()
    return render_template("account.html", current_user=current_user)
