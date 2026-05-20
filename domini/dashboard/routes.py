from flask import Blueprint, redirect, render_template, url_for
from flask_login import login_required


dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.route("/")
def home():
    return redirect(url_for("dashboard.index"))


@dashboard_bp.route("/dashboard")
@login_required
def index():
    return render_template("dashboard.html")
