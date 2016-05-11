"""Breadcrumbs: Tracking a user's restaurant history"""

from jinja2 import StrictUndefined

from flask import Flask, render_template, redirect, request, flash, session
from flask_debugtoolbar import DebugToolbarExtension

from model import User, Restaurant, Visit, Category, City, RestaurantCategory, Image, Connection
from model import connect_to_db, db


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails silently.
# This is horrible. Fix this so that, instead, it raises an error.
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage."""

    return render_template("homepage.html")


@app.route("/login", methods=["POST"])
def login():
    """Check if user's email matches password to login, otherwise ask user to try again."""

    return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out."""

    return redirect("/")


@app.route("/signup")
def signup():
    """Check if user exists in database, otherwise add user to database."""

    return render_template("signup.html")


@app.route("/users")
def user_list():
    """Show list of users."""

    return render_template("user_list.html")


@app.route("/users/<int:user_id>")
def user_profile(user_id):
    """Show user profile with map and list of visited restaurants."""

    return render_template("user_profile.html")


@app.route("/restaurants")
def restaurant_list():
    """Show list of movies."""

    return render_template("restaurant_list.html")


@app.route("/restaurants/<int:rest_id>")
def restaurant_profile(rest_id):
    """Show restaurant information."""

    return render_template("restaurant_profile.html")


@app.route("/restaurants/search")
def search_restaurants():
    """Search for a restaurant."""

    return redirect("/")


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run()
