from flask import Flask, redirect, url_for, render_template, request, session, flash
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy
import uuid

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
    id = db.Column(db.String(32), primary_key=True)
    user = db.Column(db.String(64), nullable=False)
    content = db.Column(db.String(128), nullable=False)
    complete = db.Column(db.Boolean, nullable=False)

    def __init__(self, user, content):
        self.id = str(uuid.uuid4())
        self.user = user
        self.content = content
        self.complete = False

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
    
@app.route("/logout")
def logout():
    if "user" in session:
        session.pop("user", None)
        flash("You have been logged out", "info")
    return redirect(url_for("login"))

@app.route("/list")
def list():
    if "user" not in session:
        flash("You are not logged in", "warning")
        return redirect(url_for("login"))
    user = session["user"]

    todos = todo.query.filter_by(user= user).all()
    return render_template("list.html", name= user, todos= todos)

@app.route("/add", methods=["POST"])
def add():
    if "user" not in session:
        flash("You are not logged in", "warning")
        return redirect(url_for("login"))
    
    content = request.form.get("content", "").strip()
    if content:
        item = todo(session["user"], content)
        db.session.add(item)
        db.session.commit()
        flash("Todo added", "success")
    else:
        flash("Cannot add empty todo", "warning")
    
    return redirect(url_for("list"))

@app.route("/remove/<todo_id>")
def remove(todo_id):
    if "user" not in session:
        flash("You are not logged in", "warning")
        return redirect(url_for("login"))
    
    item = todo.query.filter_by(id=todo_id, user=session["user"]).first()
    if item:
        db.session.delete(item)
        db.session.commit()
        flash("Todo deleted", "success")
    else:
        flash("Todo not found", "danger")
    
    return redirect(url_for("list"))

@app.route("/toggle/<todo_id>")
def toggle(todo_id):
    if "user" not in session:
        flash("You are not logged in", "warning")
        return redirect(url_for("login"))
    
    item = todo.query.filter_by(id=todo_id, user=session["user"]).first()
    if item:
        item.complete = not item.complete
        db.session.commit()
        flash("Todo updated", "success")
    else:
        flash("Todo not found", "danger")
    
    return redirect(url_for("list"))    

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug= True)