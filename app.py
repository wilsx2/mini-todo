from flask import Flask, redirect, url_for

app = Flask(__name__)

@app.route("/")
def root():
    return redirect(url_for("login"))

@app.route("/login")
def login():
    return "<h1>hallo</h1>"

@app.route("/list/<name>")
def tdlist(name):
    return f"Hello {name}"



if __name__ == "__main__":
    app.run()