# Team Pencil (Ari Schechter, Ethan Machleder, William Li)
# SoftDev
# P3: potential-eureka
# 2021-04-29

from flask import Flask, render_template, redirect, request, session
import urllib.request
from db_manager import *
import json
import os

app = Flask(__name__)
app.secret_key = os.urandom(32)

# creates db tables
create_tables()

EDAMAM_ID = open("keys/edamamid.txt", "r").read()
EDAMAM_KEY = open("keys/key.txt", "r").read()


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

@app.route("/recipes", methods=["GET"])
def recipes():
    fruit = request.args.get('fruit')

    with urllib.request.urlopen("https://api.edamam.com/search?q=" + fruit + "&app_id=" + EDAMAM_ID + "&app_key=" + EDAMAM_KEY + "&from=0&to=5") as response:
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


    return render_template("recipes.html", fruit=fruit, recipe_data=recipe_list)


@app.route("/saveRecipe", methods=["GET"])
def saveRecipe():
    fruit = request.args.get("fruit")
    recipe_name = request.args.get("name")
    recipe_image_url = request.args.get("image")
    recipe_url = request.args.get("url")
    ingredients = request.args.get("ingredients")

    print(recipe_image_url)
    add_favorites(session['user_id'], recipe_name, recipe_url, recipe_image_url, ingredients)
    print("Recipe saved!")
    return redirect("/recipes?fruit={}".format(fruit))


@app.route("/removeRecipe", methods=["GET"])
def removeRecipe():
    recipe_name = request.args.get("name")

    remove_favorites(session['user_id'], recipe_name)
    print("Recipe successfully deleted!")

    return redirect("/myRecipes")


@app.route("/myRecipes")
def myRecipes():
    recipe_data = get_favorites(session['user_id'])
    recipe_list = []
    for recipe in recipe_data:
        recipe_dict = {}
        recipe_dict['name'] = recipe[0]
        recipe_dict['url'] = recipe[1]
        recipe_dict['image_url'] = recipe[2]
        recipe_ingredients = recipe[3].split(', ')
        recipe_dict['ingredients'] = recipe_ingredients
        recipe_list.append(recipe_dict)
    
    return render_template("myrecipes.html", recipe_data=recipe_list)


# @app.route("/fruits")
# def fruits():
#     with urllib.request.urlopen("http://api.tropicalfruitandveg.com/tfvjsonapi.php?tfvitem={}".format("banana")) as response:
#         data = response.read()
#         strdata = str(data)
#         sliced_data = strdata[2:len(strdata) - 3].replace("\\", "")
#         data_dict = json.loads(sliced_data)
#         # json_data = json.loads(data)

#     return render_template("fruits.html", json_data=data_dict)

"""
We wanted to include a third api (the one above) but it is poorly made and 
we could not find a way to get the json data to load properly. We tried
turning it into a string and manipulating it but we simply didn't have 
enough time to find a good solution.
"""


@app.route("/logout")
def logout():
    session.pop('username')
    session.pop('password')
    session.pop('user_id')
    return redirect("/")

if __name__ == "__main__":
    app.debug = True
    app.run()