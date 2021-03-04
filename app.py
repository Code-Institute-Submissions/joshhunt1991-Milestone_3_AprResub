# Necessary imports-----------------
import os
import requests
import json
import bson
from flask import (
    Flask, flash, render_template,
    redirect, request, session, url_for)
from flask_pymongo import PyMongo
import re
from flask_paginate import Pagination, get_page_args
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
if os.path.exists("env.py"):
    import env
import uuid

# validation functions


def check_id(id):
    # Validate if id is in right format for MongoDB object.
    return bson.objectid.ObjectId.is_valid(id)


def check_name(name):
    # Validates users names.
    # Only allow letters and hyphens.  No spaces.
    return re.match("^[a-zA-Z-]{0,30}$", name)


def check_gamename(name):
    # Validates users names.
    # Only allow letters and hyphens.  No spaces.
    return re.match("^[a-zA-Z- ]{0,30}$", name)


def check_pw(pw):
    # Validate users passwords.
    # Allow any characters, length 6-15 characters only.
    return re.match("^.{6,15}$", pw)


def check_score(score):
    # Validation meter id.
    # Allow only numbers, no spaces, must be length of 13 characters.
    return re.match("^[0-5]{1}$", score)


def check_review(text):
    # Validate text input for the review page.
    # Allow any characters, length 10-250 characters only.
    return re.match("^.{10,250}$", text)


# global variables
savedImages = 0
spare_id = 0

# user agent header for api requests----
headers = {
    'User-Agent': 'VGReviewApp',
}

# Created an instance of flask--------
app = Flask(__name__)

# App configuration-------------------
app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")

# Set up an instance of PyMongo---------
mongo = PyMongo(app)

# routes--------------------------------

# route for the landing page


@app.route("/")
@app.route("/landing_page")
def landing_page():
    return render_template("index.html")

# route for the about page


@app.route("/about")
def about():
    return render_template("about.html")

# route for registration page


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":

        # Validate the data the user has provided is correct.
        if request.form.get("username") == "" or not check_name(
           request.form.get("username").lower()):
            flash("username contains invalid character.")
            return redirect(url_for("register"))
        if request.form.get("password") == "" or not check_pw(
           request.form.get("password")):
            flash("Please enter a valid password.")
            return redirect(url_for("register"))

        # check if username exists in mongodb
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})

        if existing_user:
            flash("Sorry, Someone already has that username!")
            return redirect(url_for("register"))

        register = {
            "username": request.form.get("username").lower(),
            "password": generate_password_hash(request.form.get("password"))
        }
        mongo.db.users.insert_one(register)

        # put the new user into 'session' cookie
        session["user"] = request.form.get("username").lower()
        flash("You have successfully registered!")
        return redirect(url_for("home", username=session["user"]))

    return render_template("register.html")


# route for login page


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":

        # Validate the data the user has provided.
        if request.form.get("username") == "" or not check_name(
           request.form.get("username").lower()):
            flash("Please enter a valid username.")
            return redirect(url_for("login"))
        if request.form.get("password") == "" or not check_pw(
           request.form.get("password")):
            flash("Please enter a valid password.")
            return redirect(url_for("login"))

        # check if username exists in db
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})

        if existing_user:
            # ensure hashed password matches user input
            if check_password_hash(
                    existing_user["password"], request.form.get("password")):
                session["user"] = request.form.get("username").lower()
                flash("Welcome, {}".format(
                    request.form.get("username")))
                return redirect(url_for(
                    "home", username=session["user"]))
            else:
                # invalid password match
                flash("Incorrect Username and/or Password")
                return redirect(url_for("login"))

        else:
            # username doesn't exist
            flash("Incorrect Username and/or Password")
            return redirect(url_for("login"))

    return render_template("login.html")

# route for the logged in home page


@app.route("/home/<username>", methods=["GET", "POST"])
def home(username):
    # retrieve the session user's username from db
    username = mongo.db.users.find_one(
        {"username": session["user"]})["username"]
    limit = 20
    games = mongo.db.games.find().limit(limit)

    if session["user"]:
        return render_template("home.html", username=username, games=games)

    return redirect(url_for("login"))


# app route for logging out


@app.route("/logout")
def logout():
    # remove user from session cookie
    flash("You have been logged out")
    session.pop("user")
    return redirect(url_for("login"))


# app route for review page


@app.route("/reviews")
def reviews():
    page, per_page, offset = get_page_args(page_parameter='page', per_page_parameter='per_page')

    per_page = 3
    offset = (page - 1) * per_page

    total = mongo.db.games.find().count()

    print(total)
    print(page, per_page, offset)

    findGames = mongo.db.games.find().sort("_id", -1)

    paginatedGames = findGames[offset: offset + per_page]

    print(paginatedGames)

    pagination = Pagination(page=page, per_page=per_page, total=total)
    print(page, per_page, offset)

    return render_template('reviews.html',
                           games=paginatedGames,
                           page=page,
                           per_page=per_page,
                           pagination=pagination,
                           )

# app route for profile_review page


@app.route("/profile_reviews")
def profile_reviews():
    page, per_page, offset = get_page_args(page_parameter='page', per_page_parameter='per_page')

    per_page = 3
    offset = (page - 1) * per_page
    user = session["user"]

    total = mongo.db.games.find({"created_by": user}).count()

    print(total)
    print(page, per_page, offset)
    print(user)

    findGames = mongo.db.games.find({"created_by": user}).sort("_id", -1)

    paginatedGames = findGames[offset: offset + per_page]

    print(paginatedGames)

    pagination = Pagination(page=page, per_page=per_page, total=total)
    print(page, per_page, offset)

    return render_template('profile_reviews.html',
                           games=paginatedGames,
                           page=page,
                           per_page=per_page,
                           pagination=pagination,
                           )


# app route for adding a review

@app.route("/add_game", methods=["GET", "POST"])
def add_game():
    if request.method == "POST" and session["user"]:

        # Validate the data the user has provided is correct.
        if request.form.get("game_name") == "" or not check_gamename(
           request.form.get("game_name").lower()):
            flash("Please enter a valid game name.")
            return redirect(url_for("add_game"))
        if request.form.get("rating") == "" or not check_score(
           request.form.get("rating").lower()):
            flash("Please enter a valid score.")
            return redirect(url_for("add_game"))
        if request.form.get("review") == "" or not check_review(
           request.form.get("review")):
            flash("Review does not meet the requirements please enter between 10-250 characters.")
            return redirect(url_for("add_game"))

        game_name = request.form.get("game_name")
        global spare_id
        spare_id = uuid.uuid4().hex.upper()
        game = {
            "game_name": request.form.get("game_name"),
            "rating": request.form.get("rating"),
            "review": request.form.get("review"),
            "created_by": session["user"],
            "spare_id": spare_id
        }

        url = "https://rawg-video-games-database.p.rapidapi.com/games?search=" + game_name

        headers = {
            'x-rapidapi-key': "e820b60717mshf9de36d3c2a66b8p16a209jsnbbb441546d84",
            'x-rapidapi-host': "rawg-video-games-database.p.rapidapi.com"
            }


        response = requests.request("GET", url, headers=headers)
        data = json.loads(response.text)
        mongo.db.games.insert_one(game)

        global savedImages
        savedImages = data
        print(savedImages)

        print(session["user"])

        return redirect(url_for("game_images"))

    return render_template("add_game.html")

# app route for images page


@app.route("/game_images")
def game_images():
    game = mongo.db.games.find_one({"_id": ObjectId()})
    print(game)
    return render_template("game_images.html", savedImages=savedImages)

# app route for adding image and release date


@app.route("/add_image", methods=["GET", "POST"])
def add_image():
    if request.method == 'POST' and session["user"]:
        image_url = request.form.get('image_url')
        released = request.form.get('released')
        print(image_url)
        print(released)
        print(spare_id)
        gameValues = mongo.db.games.find_one({"spare_id": spare_id})
        print(gameValues)
        mongo.db.games.update({"spare_id": spare_id}, {"$set": {"background_image": image_url}})
        mongo.db.games.update({"spare_id": spare_id}, {"$set": {"released": released}})
        flash("Review Successfully Added")

        return redirect(url_for("reviews"))

# app route for editing review


@app.route("/edit_game/<game_id>", methods=["GET", "POST"])
def edit_game(game_id):
    game_name = request.form.get("game_name")
    global spare_id
    spare_id = uuid.uuid4().hex.upper()
    submit = {
        "game_name": request.form.get("game_name"),
        "rating": request.form.get("rating"),
        "review": request.form.get("review"),
        "created_by": session["user"],
        "spare_id": spare_id
        }
    if request.method == "POST":
        if session["user"] == submit["created_by"] or session["user"] == "admin":

            url = "https://rawg-video-games-database.p.rapidapi.com/games?search=" + game_name

            headers = {
                'x-rapidapi-key': "e820b60717mshf9de36d3c2a66b8p16a209jsnbbb441546d84",
                'x-rapidapi-host': "rawg-video-games-database.p.rapidapi.com"
                }

            response = requests.request("GET", url, headers=headers)
            data =json.loads(response.text)
            mongo.db.games.update({"_id": ObjectId(game_id)}, submit)

            global savedImages
            savedImages = data

            return redirect(url_for("game_images"))

    game = mongo.db.games.find_one({"_id": ObjectId(game_id)})
    return render_template("edit_game.html", game=game)


# app route to delete a review


@app.route("/delete_game/<game_id>")
def delete_game(game_id):
    game = mongo.db.games.find_one({"_id": ObjectId(game_id)})
    if session["user"] == game["created_by"] or session["user"] == "admin":
        mongo.db.games.remove({"_id": ObjectId(game_id)})
        flash("Review Successfully Deleted")
        return redirect(url_for("reviews"))

# app route to search reviews


@app.route("/search", methods=["GET", "POST"])
def search():
    games = ""
    print(games)
    if request.method == "POST":

        query = request.form.get("query")
        print(query)
        games = list(mongo.db.games.find({"$text": {"$search": query}}))
        print(games)

    return render_template("search.html", games=games)


# error handling


@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404

# Get IP and Port data----------


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
