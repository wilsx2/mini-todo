from flask import Flask, redirect, url_for, render_template, request, session
from datetime import timedelta

app = Flask(__name__)
app.secret_key = "reallyfriggincoolman"
app.permanent_session_lifetime = timedelta(days= 1)

@app.route("/")
def root():
    return redirect(url_for("login"))

@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        session.permanent = True
        user = request.form["username"]
        session["user"] = user;
        return redirect(url_for("tdlist"))
    else:
        return render_template("login.html")

@app.route("/list")
def tdlist():
    if "user" in session:
        user = session["user"]
        return render_template("list.html", name= user)
    return redirect(url_for("login"))

@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug= True)