from flask import Flask, render_template, redirect

app = Flask(__name__)

@app.route("/")
def index():
    return redirect("/login")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/signup")
def signup():
    return render_template("signup.html")

if __name__ == "__main__":
    app.debug = True
    app.run()