from flask import Blueprint, request, render_template, session, flash, redirect, url_for
from .models import User, db


authBP = Blueprint("authBP", __name__, template_folder="templates", static_folder="static")

@authBP.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        enteredEmail = request.form["email"]
        enteredPass = request.form["pass"]        
        foundUser = User.query.filter_by(email=enteredEmail, password=enteredPass).first()
        if foundUser:
            flash("Login successfull!")
            return redirect(url_for("authBP.view"))
        else:
            flash("Account doesn't exist, create it")
            return redirect(url_for("authBP.register"))
    else:
        return render_template("login.html")

@authBP.route("register", methods=["POST", "GET"])
def register():
    if request.method == "POST":
        createdEmail = request.form["email"]
        pass1 = request.form["pass1"]
        pass2 = request.form["pass2"]

        foundUser = User.query.filter_by(email=createdEmail).first()
        if foundUser:
            flash("Email already has an account")
            return redirect(url_for("authBP.login"))
        else:                   
            if pass1 == pass2:
                session["emailKey"] = createdEmail
                session["passKey"] = pass1

                account = User(createdEmail, pass1)
                db.session.add(account)
                db.session.commit()

                return redirect(url_for("authBP.login")) 
            else:
                flash("Passwords are not the same!")
                return render_template("register.html")
    else:
        return render_template("register.html")

@authBP.route("/view")
def view():
    return render_template("view.html", values=User.query.all())