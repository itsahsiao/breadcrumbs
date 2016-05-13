"""Breadcrumbs: Tracking a user's restaurant history"""

from jinja2 import StrictUndefined

from flask import Flask, render_template, redirect, request, flash, session
from flask_debugtoolbar import DebugToolbarExtension

from model import User, Restaurant, Visit, Category, City, RestaurantCategory, Image, Connection
from model import connect_to_db, db

import os


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

    # Query to get all users
    users = db.session.query(User).all()

    return render_template("user_list.html", users=users)


# Use /user-profile for now to test Google Maps API
@app.route("/user-profile")
def user_profile():
    """Show user profile with map and list of visited restaurants."""

    user_visits = db.session.query(Visit).filter(Visit.user_id == 1).all()

    # google_key = os.environ["GOOGLE_MAPS_KEY"]

    return render_template("user_profile.html", user_visits=user_visits)
    # , google_key=google_key)


# @app.route("/users/<int:user_id>")
# def user_profile(user_id):
#     """Show user profile with map and list of visited restaurants."""

#     return render_template("user_profile.html")


@app.route("/restaurants")
def restaurant_list():
    """Show list of restaurants."""

    # Query to get all restaurants, sorted alphabetically
    restaurants = db.session.query(Restaurant).order_by(Restaurant.name).all()

    return render_template("restaurant_list.html", restaurants=restaurants)


@app.route("/restaurants/<int:restaurant_id>")
def restaurant_profile(restaurant_id):
    """Show restaurant information."""

    # Query by restaurant id to return the record from the database and access its attributes
    restaurant = db.session.query(Restaurant).filter(Restaurant.restaurant_id == restaurant_id).one()

    return render_template("restaurant_profile.html", restaurant=restaurant)


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
