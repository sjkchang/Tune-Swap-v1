from flask import current_app as app
from flask import render_template, redirect, url_for
from flask_login import (
    login_user,
    current_user,
    login_manager,
    login_required,
    logout_user,
)
from ..forms.login_form import LoginForm
from ..forms.register_form import RegistrationForm
from .. import login_manager, bcrypt
from ..models.user_model import User


@app.route("/")
def home():
    """
    Route for the home page, Home page displays current user info and a welcome.
    """
    return render_template("home.html", current_user=current_user)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Page for loging in"""
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password_hash, form.password.data):
            login_user(user)
            return redirect(url_for("home"))
    return render_template("login.html", form=form)


@app.route("/logout")
@login_required
def logout():
    """Route for login out"""
    logout_user()
    return redirect(url_for("login"))


@app.route("/register", methods=["GET", "POST"])
def register():
    """Page for Registering new user"""
    if current_user.is_authenticated:
        redirect(url_for("home"))
    form = RegistrationForm()
    if form.validate_on_submit():
        User.create(form.username.data, form.email.data, form.password.data)
        return redirect(url_for("login"))
    return render_template("register.html", form=form)
