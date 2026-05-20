from flask import Blueprint, flash, g, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user

from domini.extensions import db
from domini.models.user import User


auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard.index"))

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for("dashboard.index"))
        flash(g.t["invalid_credentials"], "error")

    return render_template("login.html")


@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))


@auth_bp.route("/register", methods=["GET", "POST"])
@login_required
def register():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        if User.query.filter_by(username=username).first():
            flash(g.t["user_exists"], "error")
        elif username and password:
            user = User(username=username)
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
            flash(g.t["user_created"], "success")
            return redirect(url_for("dashboard.index"))

    return render_template("login.html", register_mode=True)
