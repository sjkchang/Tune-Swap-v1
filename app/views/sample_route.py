from __future__ import print_function
from flask import current_app as app
from flask import render_template


@app.route("/")
def home():
    """
    Route for the home page, Home page displays current user info and a welcome.
    """
    return render_template("index.html")
