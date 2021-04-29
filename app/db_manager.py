# Team Pencil (Ari Schechter, Ethan Machleder, William Li)
# SoftDev
# P3: potential-eureka
# 2021-04-29

import sqlite3

DB_FILE = "fruits.db"

db = sqlite3.connect(DB_FILE, check_same_thread=False)
c = db.cursor()

def create_tables():

    command = "CREATE TABLE IF NOT EXISTS users(username TEXT, password TEXT, id INTEGER PRIMARY KEY AUTOINCREMENT);"

    command += "CREATE TABLE IF NOT EXISTS recipes(user_id INT, recipe_name TEXT, recipe_url TEXT, recipe_image_url TEXT, recipe_ingredients TEXT);"

    c.executescript(command)
    db.commit()


def getUserInfo(username):
    # pass a username, return correct password and user id
    command = 'SELECT username, password, id FROM users WHERE username = "{}";'.format(username)
    info = ()
    for row in c.execute(command):
        info += (row[0], row[1], row[2])
    if info == ():
        return None
    return info


def registerUser(username, password):
    # pass a username and password and have them inserted into the db
    command = 'INSERT INTO users VALUES ("{}", "{}", NULL);'.format(username, password)
    c.execute(command)
    db.commit()


def checkLogin(username, password):
    # pass a username and password and return whether 
    # or not the login was successful as well as the user id and an error if unsuccessful
    info = getUserInfo(username)
    if info is None:
        return (False, "Username not found", None)
    if username == info[0] and password == info[1]:
        return (True, "", info[2])
    return (False, "Username or password incorrect", info[2])


def add_favorites(user, rname, url, imageURL, ingredients):
    insert = "INSERT INTO recipes (user_id, recipe_name, recipe_url, recipe_image_url, recipe_ingredients) VALUES (?, ?, ?, ?, ?);"
    data=(user, rname, url, imageURL, ingredients)
    c.execute(insert, data)
    db.commit()

def get_favorites(user):
    userID=user
    c.execute('SELECT recipe_name, recipe_url, recipe_image_url, recipe_ingredients FROM recipes WHERE user_id=?', (userID,))
    data=c.fetchall()
    return data

def remove_favorites(user, rname):
    command = 'DELETE FROM recipes WHERE user_id = {} AND recipe_name = "{}";'.format(user, rname)
    c.execute(command)
    db.commit()
