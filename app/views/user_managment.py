from flask import current_app as app
from flask import render_template


@app.route("/login")
def login():
    """
    Route for the home page, Home page displays current user info and a welcome.
    """
    return render_template("login.html")
