from flask import current_app as app
from flask import render_template, session


@app.route("/")
def home():
    code = session["spotify_code"]
    access_token = session["spotify_token"]
    return render_template("home.html", code=code, access_token=access_token)