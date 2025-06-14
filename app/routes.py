from flask import Blueprint, render_template, request, redirect, url_for, session, g, flash
from werkzeug.security import generate_password_hash, check_password_hash
from .models import db, User
from datetime import datetime

main = Blueprint("main", __name__)

@main.before_app_request
def load_logged_in_user():
    g.user = session.get("user")
    g.role = session.get("role")

@main.route("/")
def index():
    return render_template("index.html")

@main.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        display_name = request.form["display_name"]
        role = "technician"  # default role

        if User.query.filter_by(username=username).first():
            flash("Username already exists.")
            return redirect(url_for("main.register"))

        hashed_pw = generate_password_hash(password)
        new_user = User(username=username, password=hashed_pw, role=role, display_name=display_name)
        db.session.add(new_user)
        db.session.commit()
        flash("Registration successful. Please log in.")
        return redirect(url_for("main.login"))

    return render_template("register.html")

@main.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            session["user"] = user.username
            session["role"] = user.role
            user.last_login = datetime.utcnow()
            db.session.commit()
            return redirect(url_for("main.index"))
        else:
            flash("Invalid credentials.")

    return render_template("login.html")

@main.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out.")
    return redirect(url_for("main.login"))
