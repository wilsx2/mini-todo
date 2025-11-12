from flask import Flask, redirect, url_for, render_template, request

app = Flask(__name__)

@app.route("/")
def root():
    return redirect(url_for("login"))

@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        return redirect(url_for("tdlist", usr= username))
    else:
        return render_template("login.html")

@app.route("/list/<usr>")
def tdlist(usr):
    return render_template("list.html", name= usr)


if __name__ == "__main__":
    app.run(debug= True)