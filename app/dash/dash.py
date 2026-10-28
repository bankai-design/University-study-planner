from flask import Blueprint, request, render_template, session, flash, redirect, url_for

dashBP = Blueprint("dashBP", __name__, template_folder="templates", static_folder="static")

@dashBP.route("/dashboard", methods=["POST", "GET"])
def dashboard():
    if request.method == "POST":
        pass
    else:
        return render_template("dashboard.html")