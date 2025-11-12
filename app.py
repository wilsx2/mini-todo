from flask import Flask, redirect, url_for, render_template

app = Flask(__name__)

@app.route("/")
def root():
    return redirect(url_for("login"))

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/list/<name>")
def tdlist(name):
    return render_template("list.html", name= name)


if __name__ == "__main__":
    app.run(debug= True)