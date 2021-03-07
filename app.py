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
    # Allow letters and hyphens but no spaces.
    return re.match("^[a-zA-Z-]{0,30}$", name)


def check_gamename(name):
    # Validates game names.
    # Allow letters and hyphens but no spaces.
    return re.match("^[a-zA-Z- ]{0,30}$", name)


def check_pw(pw):
    # Validate users passwords.
    # Allow any characters, 6-15 characters in length.
    return re.match("^.{6,15}$", pw)


def check_score(score):
    # Validation meter id.
    # Allow only numbers, no spaces, must be length of 13 characters.
    return re.match("^[0-5]{1}$", score)


def check_review(text):
    # Validate text input for the review page.
    # Allow any characters, 10-250 characters in length.
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
            flash("username contains invalid character or is too long.")
            return redirect(url_for("register"))
        if request.form.get("password") == "" or not check_pw(
           request.form.get("password")):
            flash("Please enter a valid password.")
            return redirect(url_for("register"))

        # check if username exists in mongodb
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})
        # display flash message if user already exists
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
    # send user to the logged in homepage if their username is valid
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
    # set flask paginate parameters for generating pages
    page, per_page, offset = get_page_args(
        page_parameter='page', per_page_parameter='per_page')
    per_page = 3
    offset = (page - 1) * per_page
    total = mongo.db.games.find().count()

    # generate a list of games
    findGames = mongo.db.games.find().sort("_id", -1)
    # paginate the list of games
    paginatedGames = findGames[offset: offset + per_page]
    # create the pagination variable for flask paginate
    pagination = Pagination(page=page, per_page=per_page, total=total)
    # render the template and pass through all relevant variables
    return render_template('reviews.html',
                           games=paginatedGames,
                           page=page,
                           per_page=per_page,
                           pagination=pagination,
                           )

# app route for profile_review page


@app.route("/profile_reviews")
def profile_reviews():
    # set flask paginate parameters for generating pages
    page, per_page, offset = get_page_args(
        page_parameter='page', per_page_parameter='per_page')
    per_page = 3
    offset = (page - 1) * per_page
    # create a user variable to use when searching for the users mongodb reviews
    user = session["user"]
    # find a total game count for pagination purposes
    total = mongo.db.games.find({"created_by": user}).count()
    # create a list of games
    findGames = mongo.db.games.find({"created_by": user}).sort("_id", -1)
    # paginate the games
    paginatedGames = findGames[offset: offset + per_page]
    # create pagination variable for flask paginate
    pagination = Pagination(page=page, per_page=per_page, total=total)
    # render template and pass through all the relevant variables
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

        # Validate the data the user has provided is correct if not provide flash messages to the user
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
            flash(
                "Review does not meet the requirements please enter between 10-250 characters.")
            return redirect(url_for("add_game"))
        # retrieve form data to be posted to mongodb
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
        # create a URL to contact rawg api using the game name as a search parameter
        url = "https://rawg-video-games-database.p.rapidapi.com/games?search=" + game_name
        # necessary headers for the api
        headers = {
            'x-rapidapi-key': "e820b60717mshf9de36d3c2a66b8p16a209jsnbbb441546d84",
            'x-rapidapi-host': "rawg-video-games-database.p.rapidapi.com"
        }
        # retrieve a response from the api and convert it to json
        response = requests.request("GET", url, headers=headers)
        data = json.loads(response.text)
        # post the review to mongodb
        mongo.db.games.insert_one(game)
        # create a global variable to be passed to other functions for extracting images and other relevant data
        global savedImages
        savedImages = data

        return redirect(url_for("game_images"))

    return render_template("add_game.html")

# app route for images page


@app.route("/game_images")
def game_images():
    game = mongo.db.games.find_one({"_id": ObjectId()})
    return render_template("game_images.html", savedImages=savedImages)

# app route for adding image and release date


@app.route("/add_image", methods=["GET", "POST"])
def add_image():
    if request.method == 'POST' and session["user"]:
        # when the image is clicked retrieve the image url and the release date
        image_url = request.form.get('image_url')
        released = request.form.get('released')
        # search for the relevant review by ID and add the image and release date
        mongo.db.games.update({"spare_id": spare_id}, {
                              "$set": {"background_image": image_url}})
        mongo.db.games.update({"spare_id": spare_id}, {
                              "$set": {"released": released}})
        flash("Review Successfully Added")

        return redirect(url_for("reviews"))

# app route for editing review


@app.route("/edit_game/<game_id>", methods=["GET", "POST"])
def edit_game(game_id):
    # validate the id before creating a variable to use to update the database
    if check_id(game_id):
        game_name = request.form.get("game_name")
        global spare_id
        # create a unique id to be used for searching mongodb
        spare_id = uuid.uuid4().hex.upper()
        submit = {
            "game_name": request.form.get("game_name"),
            "rating": request.form.get("rating"),
            "review": request.form.get("review"),
            "created_by": session["user"],
            "spare_id": spare_id
        }
    # if check_id fails to create a submit variable then the user is redirected to the review page and showed a flash message
    if not submit:
        flash("Your review id doesn't exist")
        return redirect(url_for("reviews"))

    if request.method == "POST":
        # check that the user is the creator of the review or the admin
        if session["user"] == submit["created_by"] or session["user"] == "admin":
            # create a url for searching the api that takes the game name as a search parameter
            url = "https://rawg-video-games-database.p.rapidapi.com/games?search=" + game_name
            # necessary headers for using the rawg api
            headers = {
                'x-rapidapi-key': "e820b60717mshf9de36d3c2a66b8p16a209jsnbbb441546d84",
                'x-rapidapi-host': "rawg-video-games-database.p.rapidapi.com"
            }
            # retrieve a response from the api and convert it to json
            response = requests.request("GET", url, headers=headers)
            data = json.loads(response.text)
            # update the database
            mongo.db.games.update({"_id": ObjectId(game_id)}, submit)
            # update the saved images variable
            global savedImages
            savedImages = data

            return redirect(url_for("game_images"))

    game = mongo.db.games.find_one({"_id": ObjectId(game_id)})
    return render_template("edit_game.html", game=game)


# app route to delete a review


@app.route("/delete_game/<game_id>")
def delete_game(game_id):
    if check_id(game_id):
        game = mongo.db.games.find_one({"_id": ObjectId(game_id)})
    # if the session user created the game or is admin then the game will be deleted
    if game:
        if session["user"] == game["created_by"] or session["user"] == "admin":
            mongo.db.games.remove({"_id": ObjectId(game_id)})
            flash("Review Successfully Deleted")
            return redirect(url_for("reviews"))
    # If there is no review found with the game_id passed through
    # return user to review page and display a flash message.
    flash("Your booking has already been deleted")
    return redirect(url_for("reviews"))

# app route to search reviews


@app.route("/search", methods=["GET", "POST"])
def search():
    # create an empty games variable to populate with search results
    games = ""
    # when the post method is used create a search query variable and use that to update the games variable with search results
    if request.method == "POST":

        query = request.form.get("query")
        games = list(mongo.db.games.find({"$text": {"$search": query}}))
    # if no search is found display a flash message
        if not games:
            flash("sorry, no matching search was found")
            return redirect(url_for("search"))

    return render_template("search.html", games=games)


# error handling for missing pages


@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404

# Get IP and Port data----------


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
