from flask import Flask, redirect, url_for, render_template, request, session, flash
from datetime import timedelta

app = Flask(__name__)
app.secret_key = "reallyfriggincoolman"
app.permanent_session_lifetime = timedelta(days= 1)

@app.route("/")
def root():
    return redirect(url_for("list"))

@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        valid = True
        if not valid:
            flash("Incorrect login information", "danger");
        session.permanent = True
        user = request.form["username"]
        session["user"] = user;
        return redirect(url_for("list"))
    else:
        return render_template("login.html")

@app.route("/list")
def list():
    if "user" in session:
        user = session["user"]
        return render_template("list.html", name= user)
    flash("You are not logged in", "warning")
    return redirect(url_for("login"))

@app.route("/logout")
def logout():
    if "user" in session:
        session.pop("user", None)
        flash("You have been logged out", "info")
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug= True)