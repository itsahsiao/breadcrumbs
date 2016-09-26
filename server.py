"""Breadcrumbs: Tracking a user's restaurant history"""

import os

from jinja2 import StrictUndefined

from flask import Flask, render_template, redirect, request, flash, session, jsonify
from flask_debugtoolbar import DebugToolbarExtension

from model import User, Restaurant, Visit, Category, City, RestaurantCategory, Image, Connection
from model import connect_to_db, db

# Import SQLALchemy exception error to use in try/except
from sqlalchemy.orm.exc import NoResultFound

# Import search function from library to query for information in database
from sqlalchemy_searchable import search

# Import helper functions
from friends import is_friends_or_pending, get_friend_requests, get_friends

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get("FLASK_SECRET_KEY", "abcdef")

# Normally, if you use an undefined variable in Jinja2, it fails silently.
# This is horrible. Fix this so that, instead, it raises an error.
app.jinja_env.undefined = StrictUndefined

from raven.contrib.flask import Sentry
sentry = Sentry(app, dsn='https://c42cb440f5ce49039d750403b70d910d:d1c5986bcfe645e1963902d198ff021f@sentry.io/101473')


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
    """Log user in if credentials provided are correct."""

    login_email = request.form.get("login_email")
    login_password = request.form.get("login_password")

    # Try if credentials provided by user match record in database
    # If incorrect (NoResultFound in db), ask them to try again
    # If correct, log them in, redirecting them to their user profile
    try:
        current_user = db.session.query(User).filter(User.email == login_email,
                                                     User.password == login_password).one()
    except NoResultFound:
        flash("The email or password you have entered did not match our records. Please try again.", "danger")
        return redirect("/login")

    # Get current user's friend requests and number of requests to display in badges
    received_friend_requests, sent_friend_requests = get_friend_requests(current_user.user_id)
    num_received_requests = len(received_friend_requests)
    num_sent_requests = len(sent_friend_requests)
    num_total_requests = num_received_requests + num_sent_requests

    # Use a nested dictionary for session["current_user"] to store more than just user_id
    session["current_user"] = {
        "first_name": current_user.first_name,
        "user_id": current_user.user_id,
        "num_received_requests": num_received_requests,
        "num_sent_requests": num_sent_requests,
        "num_total_requests": num_total_requests
    }

    flash("Welcome {}. You have successfully logged in.".format(current_user.first_name), "success")

    return redirect("/users/{}".format(current_user.user_id))


@app.route("/logout")
def logout():
    """Log user out."""

    del session["current_user"]

    flash("Goodbye! You have successfully logged out.", "success")

    return redirect("/")


@app.route("/signup", methods=["GET"])
def show_signup():
    """Show signup form."""

    return render_template("signup.html")


@app.route("/signup", methods=["POST"])
def signup():
    """Check if user exists in database, otherwise add user to database."""

    signup_email = request.form.get("signup_email")
    signup_password = request.form.get("signup_password")
    first_name = request.form.get("first_name")
    last_name = request.form.get("last_name")
    city = request.form.get("city")

    city_id = db.session.query(City).filter(City.name == city).one().city_id

    # Try if signup email provided does not already exist in db
    # If email does not exist (NoResultFound in db), create new user and log them in
    # If it is an existing email, flash message to tell user to login
    try:
        db.session.query(User).filter(User.email == signup_email).one()

    except NoResultFound:
        new_user = User(city_id=city_id,
                        email=signup_email,
                        password=signup_password,
                        first_name=first_name,
                        last_name=last_name)
        db.session.add(new_user)
        db.session.commit()

        # Add same info to session for new user as per /login route
        session["current_user"] = {
            "first_name": new_user.first_name,
            "user_id": new_user.user_id,
            "num_received_requests": 0,
            "num_sent_requests": 0,
            "num_total_requests": 0
        }

        flash("You have succesfully signed up for an account, and you are now logged in.", "success")

        return redirect("/users/%s" % new_user.user_id)

    flash("An account already exists with this email address. Please login.", "danger")

    return redirect("/login")


@app.route("/users")
def user_list():
    """Show list of users."""

    users = db.session.query(User).all()

    return render_template("user_list.html",
                           users=users)


@app.route("/users/<int:user_id>")
def user_profile(user_id):
    """Show user profile with map and list of visited restaurants."""

    user = db.session.query(User).filter(User.user_id == user_id).one()

    # Get user's breadcrumbs in descending order
    breadcrumbs = db.session.query(Visit).filter(Visit.user_id == user_id).order_by(Visit.visit_id.desc())

    total_breadcrumbs = len(breadcrumbs.all())
    recent_breadcrumbs = breadcrumbs.limit(5).all()

    total_friends = len(get_friends(user.user_id).all())

    user_a_id = session["current_user"]["user_id"]
    user_b_id = user.user_id

    # Check connection status between user_a and user_b
    friends, pending_request = is_friends_or_pending(user_a_id, user_b_id)

    return render_template("user_profile.html",
                           user=user,
                           total_breadcrumbs=total_breadcrumbs,
                           recent_breadcrumbs=recent_breadcrumbs,
                           total_friends=total_friends,
                           friends=friends,
                           pending_request=pending_request)


@app.route("/users/<int:user_id>/visits.json")
def user_restaurant_visits(user_id):
    """Return info about a user's restaurant visits as JSON."""

    # Query to get all restaurant visits for a user
    user_visits = db.session.query(Visit).filter(Visit.user_id == user_id).all()

    rest_visits = {}

    for visit in user_visits:
        image_url = visit.restaurant.image_url if visit.restaurant.image_url else "/static/img/restaurant-avatar.png"
        phone = visit.restaurant.phone if visit.restaurant.phone else "Not Available"

        rest_visits[visit.visit_id] = {
            "restaurant": visit.restaurant.name,
            "rest_id": visit.restaurant.restaurant_id,
            "address": visit.restaurant.address,
            "phone": phone,
            "image_url": image_url,
            # Need to convert latitude and longitude to floats
            # Otherwise get a TypeError: Decimal is not JSON serializable
            "latitude": float(visit.restaurant.latitude),
            "longitude": float(visit.restaurant.longitude)
        }

    return jsonify(rest_visits)


@app.route("/add-friend", methods=["POST"])
def add_friend():
    """Send a friend request to another user."""

    user_a_id = session["current_user"]["user_id"]
    user_b_id = request.form.get("user_b_id")

    # Check connection status between user_a and user_b
    is_friends, is_pending = is_friends_or_pending(user_a_id, user_b_id)

    if user_a_id == user_b_id:
        return "You cannot add yourself as a friend."

    elif is_friends:
        return "You are already friends."

    elif is_pending:
        return "Your friend request is pending."

    # Add a connection to the database if above conditionals are not true
    else:
        requested_connection = Connection(user_a_id=user_a_id,
                                          user_b_id=user_b_id,
                                          status="Requested")

        db.session.add(requested_connection)
        db.session.commit()

        # This prints in the console to check
        print "User ID %s has sent a friend request to User ID %s" % (user_a_id, user_b_id)

        return "Request Sent"


@app.route("/friends")
def show_friends_and_requests():
    """Show friend requests and list of all friends"""

    # Returns users for current user's friend requests
    received_friend_requests, sent_friend_requests = get_friend_requests(session["current_user"]["user_id"])

    # Returns query for current user's friends (not User objects) so add .all() to the end to get list of User objects
    friends = get_friends(session["current_user"]["user_id"]).all()

    return render_template("friends.html",
                           received_friend_requests=received_friend_requests,
                           sent_friend_requests=sent_friend_requests,
                           friends=friends)


@app.route("/friends/search", methods=["GET"])
def search_users():
    """Search for a user by email and return results."""

    # Returns users for current user's friend requests
    received_friend_requests, sent_friend_requests = get_friend_requests(session["current_user"]["user_id"])

    # Returns query for current user's friends (not User objects) so add .all() to the end to get list of User objects
    friends = get_friends(session["current_user"]["user_id"]).all()

    user_input = request.args.get("q")

    # Search user's query in users table of db and return all search results
    search_results = search(db.session.query(User), user_input).all()

    return render_template("friends_search_results.html",
                           received_friend_requests=received_friend_requests,
                           sent_friend_requests=sent_friend_requests,
                           friends=friends,
                           search_results=search_results)


@app.route("/restaurants")
def restaurant_list():
    """Show list of restaurants."""

    # Returns all restaurants, sorted alphabetically
    restaurants = db.session.query(Restaurant).order_by(Restaurant.name).all()

    return render_template("restaurant_list.html",
                           restaurants=restaurants)


@app.route("/restaurants/search", methods=["GET"])
def search_restaurants():
    """Search for a restaurant by name or address and return results."""

    user_input = request.args.get("q")

    # Search user's query in restaurant table of db and return all search results
    search_results = search(db.session.query(Restaurant), user_input).all()

    return render_template("restaurants_search_results.html", search_results=search_results)


@app.route("/restaurants/<int:restaurant_id>")
def restaurant_profile(restaurant_id):
    """Show restaurant information."""

    restaurant = db.session.query(Restaurant).filter(Restaurant.restaurant_id == restaurant_id).one()

    # Returns query for current user's friends, not User objects
    friends = get_friends(session["current_user"]["user_id"])

    # Pass friends into this query to filter by restaurant, and join visits table to 
    # see which of user's friends have visited this restaurant
    friends_who_visited = friends.filter(Visit.restaurant_id == restaurant_id).join(Visit,
                                                                                    Visit.user_id == Connection.user_b_id).all()

    return render_template("restaurant_profile.html",
                           restaurant=restaurant,
                           friends_who_visited=friends_who_visited)


@app.route("/add-visit", methods=["POST"])
def add_visit():
    """Add restaurant visit to user's restaurant history."""

    restaurant_id = request.form.get("restaurant_id")

    # Try if user has added this restaurant previously
    # If not, add this restaurant visit to database under this user id
    # and redirect user to their profile page to see the newly added marker
    # If so, do not add restaurant visit and redirect user back to restaurant page
    try:
        db.session.query(Visit).filter(Visit.restaurant_id == restaurant_id,
                                       Visit.user_id == session["current_user"]["user_id"]).one()

    except NoResultFound:
        # Add restaurant visit to database and commit change
        visit = Visit(user_id=session["current_user"]["user_id"], restaurant_id=restaurant_id)
        db.session.add(visit)
        db.session.commit()

        flash("You just left a breadcrumb for this restaurant.", "success")

        return redirect("/users/%s" % session["current_user"]["user_id"])

    flash("You already left a breadcrumb for this restaurant.", "danger")

    return redirect("/restaurants/%s" % restaurant_id)


@app.route("/error")
def error():
    raise Exception("Error!")


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    app.debug = True

    # connect_to_db(app)
    connect_to_db(app, os.environ.get("DATABASE_URL"))
    db.create_all()

    # Use the DebugToolbar
    # DebugToolbarExtension(app)

    PORT = int(os.environ.get("PORT", 5000))
    DEBUG = "NO_DEBUG" not in os.environ

    # app.run()
    app.run(host="0.0.0.0", port=PORT, debug=DEBUG)
