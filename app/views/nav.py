from flask import current_app as app
from flask import render_template, session

from ..utils import spotify
import json
import requests


@app.route("/")
def home():
    code = "N/a"
    access_token = "n/a"
    me = "n/a"
    if session.get("code"):
        code = session["code"]
    if session.get("access_token"):
        access_token = session["access_token"]
        me = spotify.Spotify(access_token["access_token"]).get_current_user()
        print(me.json())
        me = me.json()

    return render_template("home.html", code=code, access_token=access_token, me=me)