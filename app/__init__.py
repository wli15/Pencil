from flask import Flask, render_template, redirect, request, session
from db_manager import *
import requests
import os

app = Flask(__name__)
app.secret_key = os.urandom(32)

# creates db tables
create_tables()


@app.route("/")
def index():
    # check if user already logged in
    if 'user_id' in session:
        return redirect("/home")
    return redirect("/login")


@app.route("/login")
def login():
    return render_template("login.html")


@app.route("/signup")
def signup():
    return render_template("signup.html")


@app.route("/home")
def home():
    apple_data = requests.get('https://www.fruityvice.com/api/fruit/apple')
    banana_data = requests.get('https://www.fruityvice.com/api/fruit/banana')
    strawberry_data = requests.get('https://www.fruityvice.com/api/fruit/strawberry')
    pineapple_data = requests.get('https://www.fruityvice.com/api/fruit/pineapple')
    return render_template("index.html", username=session['username'], apple_data, banana_data, strawberry_data, pineapple_data)


@app.route("/signupRequest", methods=["POST"])
def signupRequst():
    tempUser = request.form["username"]
    tempPass = request.form["password"]
    if (tempUser == "") or (tempPass == ""):
        # return an error
        return render_template("error.html", error="Input fields cannot be left blank. Please fill both in")
    registerUser(tempUser, tempPass)
    session['username'] = tempUser
    return redirect("/home")


@app.route("/loginRequest", methods=["POST"])
def loginRequest():
    tempUser = request.form['username']
    tempPass = request.form['password']
    loginS, error, user_id = checkLogin(tempUser, tempPass)
    if loginS:
        session['username'] = tempUser
        session['password'] = tempPass
        session['user_id'] = user_id
        return redirect("/home")
    # return an error
    return render_template("error.html", error=error)


@app.route("/logout")
def logout():
    session.pop('username')
    session.pop('password')
    session.pop('user_id')
    return redirect("/")

if __name__ == "__main__":
    app.debug = True
    app.run()