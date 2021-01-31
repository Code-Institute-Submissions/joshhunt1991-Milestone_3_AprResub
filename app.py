# Necessary imports-----------------
import os
from flask import (
    Flask, flash, render_template,
    redirect, request, session, url_for)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
if os.path.exists("env.py"):
    import env

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

    if session["user"]:
        return render_template("home.html", username=username)

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
    games = mongo.db.games.find()
    return render_template("reviews.html", games=games)


# app route for adding a review

@app.route("/add_game", methods=["GET", "POST"])
def add_game():
    if request.method == "POST":
        game = {
            "game_name": request.form.get("game_name"),
            "rating": request.form.get("rating"),
            "review": request.form.get("review"),
            "created_by": session["user"]
        }
        mongo.db.games.insert_one(game)
        flash("Review Successfully Added")
        return redirect(url_for("reviews"))

    categories = mongo.db.categories.find().sort("game_name", 1)
    return render_template("add_game.html", categories=categories)

# Get IP and Port data----------


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
