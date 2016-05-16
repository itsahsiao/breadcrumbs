"""Breadcrumbs: Tracking a user's restaurant history"""

from jinja2 import StrictUndefined

from flask import Flask, render_template, redirect, request, flash, session, jsonify
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


@app.route("/login", methods=["GET"])
def show_login():
    """Show login form."""

    return render_template("login.html")


@app.route("/login", methods=["POST"])
def login():
    """Check if user's email matches password to login, otherwise ask user to try again."""

    # Get values from login form
    login_email = request.form.get("login_email")
    login_password = request.form.get("login_password")

    # Check if user email and password matches
    # If so, log them in and keep user email and id in session to use elsewhere

    # TODO:
    # Ask regarding .one() and .first()
    # There should only be one record for a user???
    # Need to try/except if doing .one()?
    # OR use nested if statements?
        # If user exists in database
            # then check if password matches this user

    # import pdb; pdb.set_trace()

    if db.session.query(User).filter(User.email == login_email,
                                     User.password == login_password).first():

        current_user = User.query.filter(User.email == login_email).one()

        # Use a nested dictionary for session["current_user"] to access email and user id
        # This way, create only one session and delete only one session vs. two or more
        session["current_user"] = {
            "email": current_user.email,
            "user_id": current_user.user_id
        }

        flash("You have successfully logged in.")

        return redirect("/users/%s" % current_user.user_id)

    else:
        flash("The email or password you have entered did not match our records. Please try again.")
        return redirect("/login")


@app.route("/logout")
def logout():
    """Log user out."""

    del session["current_user"]

    flash("You have been successfully logged out.")

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


@app.route("/users/<int:user_id>")
def user_profile(user_id):
    """Show user profile with map and list of visited restaurants."""

    # Query by user id to return that record in database about user info
    user = db.session.query(User).filter(User.user_id == user_id).one()

    return render_template("user_profile.html", user=user)


@app.route("/user-visits.json")
def user_restaurant_visits():
    """Return info about user's restaurant visits as JSON."""

    # Query to get all visits for current logged in user (pass in user id from session)
    user_visits = db.session.query(Visit).filter(Visit.user_id == session["current_user"]["user_id"]).all()

    rest_visits = {}

    for visit in user_visits:
        rest_visits[visit.visit_id] = {
            "restaurant": visit.restaurant.name,
            "address": visit.restaurant.address,
            "phone": visit.restaurant.phone,
            "image_url": visit.restaurant.image_url,
            # Need to convert latitude and longitude to floats
            # Otherwise get a TypeError: Decimal is not JSON serializable
            "latitude": float(visit.restaurant.latitude),
            "longitude": float(visit.restaurant.longitude)
        }

    return jsonify(rest_visits)


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


@app.route("/add-visit/<int:restaurant_id>", methods=["POST"])
def add_restaurant():
    """Add restaurant to user's list of visited restaurants."""

    # import pdb; pdb.set_trace()
    # Get restaurant id from add form
    # restaurant = request.form.get("restaurant_id")

    # if fails (i.e. server issues), redirect back to restaurant page
    # else, add and redicect to user profile page

    return redirect("/users/<int:user_id>")
#     # Get user id from session
#     user = 

#     # Check if user has added this restaurant previously

#     # Add visit 
#     db.session.add(Visit(user_id=user, restaurant_id=restaurant))
#     db.session.commit()


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
