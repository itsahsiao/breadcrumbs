"""Breadcrumbs: Tracking a user's restaurant history"""

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

# Create Flask app
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
    """Log user in if credentials provided are correct."""

    # Get values from login form
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

    # Use a nested dictionary for session["current_user"] to store email and user id
    # This way, create only one session and delete only one session vs. two or more if want to store more info
    session["current_user"] = {
        "email": current_user.email,
        "user_id": current_user.user_id
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

    # query cities and pass into jinja for drop down menu and option value = city id

    return render_template("signup.html")


@app.route("/signup", methods=["POST"])
def signup():
    """Check if user exists in database, otherwise add user to database."""

    # Get values from signup form
    signup_email = request.form.get("signup_email")
    signup_password = request.form.get("signup_password")
    first_name = request.form.get("first_name")
    last_name = request.form.get("last_name")
    city = request.form.get("city")

    # Get city id for city name
    # TODO: Ask about object vs tuple, since can query on City.city_id and index [0] to get city id
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

        session["current_user"] = {
            "email": new_user.email,
            "user_id": new_user.user_id
        }

        flash("You have succesfully signed up for an account, and you are now logged in.", "success")

        return redirect("/users/%s" % new_user.user_id)

    flash("An account already exists with this email address. Please login.", "danger")

    return redirect("/login")


@app.route("/users")
def user_list():
    """Show list of users."""

    # Query to get all users
    users = db.session.query(User).all()

    return render_template("user_list.html",
                           users=users)


@app.route("/users/<int:user_id>")
def user_profile(user_id):
    """Show user profile with map and list of visited restaurants."""

    # Query by user id to return the user from database and access its attributes
    user = db.session.query(User).filter(User.user_id == user_id).one()

    # Get user's breadcrumbs in ascending order
    breadcrumbs = db.session.query(Visit).filter(Visit.user_id == user_id).order_by(Visit.visit_id.desc())

    # Return total # of breadcrumbs and recent 5 breadcrumbs
    total_breadcrumbs = len(breadcrumbs.all())
    recent_breadcrumbs = breadcrumbs.limit(5).all()

    # Get user_a_id (current user) and user_b_id (from user profile page)
    user_a_id = session["current_user"]["user_id"]
    user_b_id = user.user_id

    # Check connection status between user_a and user_b
    friends, pending_request = is_friends_or_pending(user_a_id, user_b_id)

    return render_template("user_profile.html",
                           user=user,
                           total_breadcrumbs=total_breadcrumbs,
                           recent_breadcrumbs=recent_breadcrumbs,
                           friends=friends,
                           pending_request=pending_request)


@app.route("/users/<int:user_id>/visits.json")
def user_restaurant_visits(user_id):
    """Return info about a user's restaurant visits as JSON."""

    # Query to get all restaurant visits for a user
    user_visits = db.session.query(Visit).filter(Visit.user_id == user_id).all()

    rest_visits = {}

    for visit in user_visits:
        image_url = visit.restaurant.image_url if visit.restaurant.image_url else "http://placehold.it/100x100?text=No+Image+Available"
        phone = visit.restaurant.phone if visit.restaurant.phone else "Not Available"

        rest_visits[visit.visit_id] = {
            "restaurant": visit.restaurant.name,
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

    # Get user_a_id (current user) from flask session and user_b_id via AJAX post request
    user_a_id = session["current_user"]["user_id"]
    user_b_id = request.form.get("user_b_id")

    # Check connection status between user_a and user_b
    is_friends, is_pending = is_friends_or_pending(user_a_id, user_b_id)

    # user_a cannot send friend request to self
    if user_a_id == user_b_id:
        return "You cannot add yourself as a friend."

    # user_a cannot send friend request to user_b if they are friends
    elif is_friends:
        return "You are already friends."

    # user_a cannot send another friend request to user_b if there is a pending request
    elif is_pending:
        return "Your friend request is pending."

    # If user_a and user_b are not friends and there is no pending request for user_b,
    # Add a connection in the database that user_a sent a friend request to user_b
    else:
        requested_connection = Connection(user_a_id=user_a_id,
                                          user_b_id=user_b_id,
                                          status="Requested")

        db.session.add(requested_connection)
        db.session.commit()

        # Print in the console to check
        print "User ID %s has sent a friend request to User ID %s" % (user_a_id, user_b_id)

        return "Request Sent"


@app.route("/friends")
def show_friends_and_requests():
    """Show friend requests and list of all friends"""

    # Get current user's friend requests
    received_friend_requests, sent_friend_requests = get_friend_requests(session["current_user"]["user_id"])

    # Query for current user's friends (returns query, not User objects)
    # Add .all() to the end to get list of User objects
    friends = get_friends(session["current_user"]["user_id"]).all()

    return render_template("friends.html",
                           received_friend_requests=received_friend_requests,
                           sent_friend_requests=sent_friend_requests,
                           friends=friends)


@app.route("/restaurants")
def restaurant_list():
    """Show list of restaurants."""

    # Query to get all restaurants, sorted alphabetically
    restaurants = db.session.query(Restaurant).order_by(Restaurant.name).all()

    return render_template("restaurant_list.html",
                           restaurants=restaurants)


@app.route("/restaurants/<int:restaurant_id>")
def restaurant_profile(restaurant_id):
    """Show restaurant information."""

    # Query by restaurant id to return the restaurant from the database and access its attributes
    restaurant = db.session.query(Restaurant).filter(Restaurant.restaurant_id == restaurant_id).one()

    # Query for current user's friends (returns query, not User objects)
    friends = get_friends(session["current_user"]["user_id"])

    # Pass friends into this query to filter by restaurant, and
    # joining the visits table to see if user's friends have visited this restaurant
    friends_who_visited = friends.filter(Visit.restaurant_id == restaurant_id).join(Visit,
                                                                                    Visit.user_id == Connection.user_b_id).all()

    return render_template("restaurant_profile.html",
                           restaurant=restaurant,
                           friends_who_visited=friends_who_visited)


@app.route("/add-visit", methods=["POST"])
def add_visit():
    """Add restaurant visit to user's restaurant history."""

    # Get restaurant id from hidden input form when user clicks "Leave a Breadcrumb" button
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


@app.route("/search", methods=["GET"])
def search_restaurants():
    """Search for a restaurant and return results."""

    # Get value from searchbox form for user's query
    user_search = request.args.get("q")

    # # Search user's query in restaurant table of db and return all search results
    # query = db.session.query(Restaurant)
    # query = search(query, user_search)
    # search_results = query.all()

    # Refactored above code to one line
    search_results = search(db.session.query(Restaurant), user_search).all()

    return render_template("search_results.html", search_results=search_results)


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run()
