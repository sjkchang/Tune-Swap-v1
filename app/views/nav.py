from flask import current_app as app
from flask import render_template, session


@app.route("/")
def home():
    code = "N/a"
    access_token = "n/a"
    if session.get("code"):
        code = session["code"]
    if session.get("access_token"):
        access_token = session["access_token"]
    return render_template("home.html", code=code, access_token=access_token)