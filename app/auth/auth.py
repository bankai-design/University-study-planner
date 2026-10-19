from flask import Blueprint, request, render_template, session, flash, redirect, url_for

authBP = Blueprint("authBP", __name__, template_folder="templates", static_folder="static")

@authBP.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["pass"]
        session["emailKey"] = email
        session["passKey"] = password
        return
    else:
        return render_template("login.html")

@authBP.route("register", methods=["POST", "GET"])
def register():
    if request.method == "POST":
        email = request.form["email"]
        pass1 = request.form["pass1"]
        pass2 = request.form["pass2"]
        if pass1 == pass2:
            session["emailKey"] = email
            session["passKey"] = pass1
            return redirect(url_for("testing"))
        else:
            flash("Passwords are not the same!")
            return render_template("register.html")
    else:
        return render_template("register.html")

@authBP.route("/")
def testing():
    return "hello, this is working"