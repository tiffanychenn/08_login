from flask import Flask, render_template, request, session, redirect, url_for
import os

jinjas_in_the_night = Flask(__name__)

jinjas_in_the_night.secret_key = os.urandom(32)

users = {"me":"pass"}

@jinjas_in_the_night.route("/", methods = ["GET", "POST"])
def root():
    if "login" in session:
        return redirect(url_for("welcome"))
    elif "pass" in session:
        session.pop("pass")
        return root(False, True)
    elif "user" in session:
        session.pop("user")
        return root(True, False)
    else:
        return root(False, False)

def root(a, b):
    return render_template("base.html", user = a, passw = b)

@jinjas_in_the_night.route("/check_creds", methods = ["GET", "POST"])
def check_creds():
    print session 
    for key in users:
        if key == request.form["user"]:
            if users[key] == request.form["passw"]:
                session["login"] = True
                return redirect(url_for("welcome"))
            else:
                session["pass"] = True
                return redirect(url_for("root"))
        else:
            session["user"] = True
            return redirect(url_for("root"))

@jinjas_in_the_night.route("/welcome", methods = ["GET", "POST"])
def welcome():
    return render_template("welcome.html")

@jinjas_in_the_night.route("/logout", methods = ["GET", "POST"])
def logout():
    session.pop("login")
    return render_template("logout.html")

if __name__ == "__main__":
    jinjas_in_the_night.debug = True
    jinjas_in_the_night.run()