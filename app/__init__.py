from flask import Flask, render_template, redirect, request, session
import urllib.request
from db_manager import *
import json
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
    fruits = ['banana', 'strawberry', 'apple', 'pineapple']
    banana_data = {}
    strawberry_data = {}
    apple_data = {}
    pineapple_data = {}
    for x in fruits:
        with urllib.request.urlopen('https://www.fruityvice.com/api/fruit/{}'.format(x)) as response:
            data = response.read()
            json_data = json.loads(data)
            del json_data['id']
            for key, value in json_data['nutritions'].items():
                if key == 'calories':
                    json_data[key] = value
                else:
                    json_data[key] = str(value) + 'g'
            del json_data['nutritions']

            if json_data['name'].lower() == 'banana':
                del json_data['name']
                banana_data = json_data
            elif json_data['name'].lower() == 'strawberry':
                del json_data['name']
                strawberry_data = json_data
            elif json_data['name'].lower() == 'apple':
                del json_data['name']
                apple_data = json_data
            elif json_data['name'].lower() == 'pineapple':
                del json_data['name']
                pineapple_data = json_data

    return render_template("index.html", username=session['username'], apple_data=apple_data, banana_data=banana_data, strawberry_data=strawberry_data, pineapple_data=pineapple_data)


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

@app.route("/recipes")
def recipes():
    fruit = request.args.get('fruit')

    with urllib.request.urlopen("https://api.edamam.com/search?q={}&app_id=377f7e36&app_key=2de86ea54eb07fb4df0a3db9fde0e3a0&from=0&to=5".format(fruit)) as response:
        data = response.read()
        json_data = json.loads(data)
        recipe_list = []
        for i in range(0, 5):
            temp_recipe = {}
            recipe_data = json_data['hits'][i]['recipe']
            temp_recipe['name'] = recipe_data['label']
            temp_recipe['url'] = recipe_data['url']
            temp_recipe['image_url'] = recipe_data['image']
            temp_recipe['ingredients'] = recipe_data['ingredientLines']
            recipe_list.append(temp_recipe)


    return render_template("recipes.html", user_id=session['user_id'], fruit=fruit, recipe_data=recipe_list)


@app.route("/logout")
def logout():
    session.pop('username')
    session.pop('password')
    session.pop('user_id')
    return redirect("/")

if __name__ == "__main__":
    app.debug = True
    app.run()