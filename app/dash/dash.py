from flask import Blueprint, request, render_template, session, flash, redirect, url_for

dashBP = Blueprint("dashBP", __name__, template_folder="templates", static_folder="static")

@dashBP.route("/dashboard")
def dashboard(user):
    return render_template("dashboard.html", user=user)

@dashBP.route("/calendar")
def calendar():
    return render_template("calendar.html")

@dashBP.route("/assignments")
def assignments():
    return render_template("assignments.html")

@dashBP.route("/studyPlan")
def studyPlan():
    return render_template("studyPlan.html")

@dashBP.route("/modules")
def modules():
    return render_template("modules.html")