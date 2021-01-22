# Necessary imports-----------------
import os
from flask import (
    Flask, flash, render_template,
    redirect, request, session, url_for)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
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

# Routes----------------------
@app.route("/")
@app.route("/landing_page")
def landing_page():
    return render_template("index.html")

# Get IP and Port data----------
if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)