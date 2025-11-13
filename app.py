from flask import Flask, redirect, url_for, render_template, request, session, flash
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "reallyfriggincoolman"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.permanent_session_lifetime = timedelta(days= 1)

db = SQLAlchemy(app)

class users(db.Model):
    username = db.Column(db.String(64), primary_key=True)
    password = db.Column(db.String(64), nullable=False)

    def __init__(self, username, password):
        self.username = username
        self.password = password
        
class todo(db.Model):
    _id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(64), nullable=False)
    content = db.Column(db.String(128), nullable=False)
    complete = db.Column(db.Boolean, nullable=False)

    def __init__(self, id, user, content, complete):
        self._id = id
        self.user = user
        self.content = content
        self.complete = complete

@app.route("/")
def root():
    return redirect(url_for("list"))

@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        found_user = users.query.filter_by(username= username).first()
        if found_user:
            if found_user.password != password:
                flash("Incorrect password", "danger");
                return render_template("login.html")
        else:
            user = users(username, password)
            db.session.add(user)
            db.session.commit()
        
        session.permanent = True
        session["user"] = username;
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
    with app.app_context():
        db.create_all()
    app.run(debug= True)