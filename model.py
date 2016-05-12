"""Models and database functions for Hackbright project (Breadcrumbs)."""

from flask_sqlalchemy import SQLAlchemy

# This is the connection to the PostgreSQL database; we're getting this through
# the Flask-SQLAlchemy helper library. On this, we can find the `session`
# object, where we do most of our interactions (like committing, etc.)

db = SQLAlchemy()

import datetime


##############################################################################
# Model definitions

class User(db.Model):
    """User of Breadcrumbs website."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    city_id = db.Column(db.Integer, db.ForeignKey('cities.city_id'), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<User user_id=%s email=%s>" % (self.user_id,
                                               self.email)


class Restaurant(db.Model):
    """Restaurant on Breadcrumbs website."""

    __tablename__ = "restaurants"

    restaurant_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    city_id = db.Column(db.Integer, db.ForeignKey('cities.city_id'), nullable=False)
    name = db.Column(db.String(150), nullable=False)
    address = db.Column(db.String(150), nullable=False)
    phone = db.Column(db.String(20), nullable=True)
    # image_url could be nullable=False if you design your data in a way that you
    # only want restaurants that have images
    image_url = db.Column(db.String(200), nullable=True)
    # Latitude and Longitude need to be Numeric, not Integer to have decimal places
    # Could exclude restaurants from your dataset that do not have latitude/longitude
    # Same thing with address
    # Note: food trucks do not have an address, but random marker...
    latitude = db.Column(db.Numeric, nullable=False)
    longitude = db.Column(db.Numeric, nullable=False)

    categories = db.relationship("Category", secondary="restaurantcategories", backref="restaurants")

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Restaurant restaurant_id=%s name=%s>" % (self.restaurant_id,
                                                          self.name)


class Visit(db.Model):
    """User's visited/saved restaurant on Breadcrumbs website.
    Association table between User and Restaurant.
    """

    __tablename__ = "visits"

    visit_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurants.restaurant_id'), nullable=False)

    # Define relationships
    user = db.relationship("User", backref=db.backref("visits"))
    restaurant = db.relationship("Restaurant", backref=db.backref("visits"))

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Visit visit_id=%s restaurant_id=%s>" % (self.visit_id,
                                                         self.restaurant_id)


class City(db.Model):
    """City where the restaurant is in."""

    __tablename__ = "cities"

    city_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    # Set default for timestamp of current time at UTC time zone
    updated_At = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    # Define relationships
    users = db.relationship("User", backref=db.backref("city"))
    restaurants = db.relationship("Restaurant", backref=db.backref("city"))

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<City city_id=%s name=%s>" % (self.city_id,
                                              self.name)


### BELOW MODELS ARE FOR ADDITIONAL FEATURES TO BE WORKED ON LATER ###

class Category(db.Model):
    """Category of the restaurant."""

    __tablename__ = "categories"

    category_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Category category_id=%s name=%s>" % (self.category_id,
                                                      self.name)


class RestaurantCategory(db.Model):
    """Association table linking Restaurant and Category to manage the M2M relationship."""

    __tablename__ = "restaurantcategories"

    restcat_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurants.restaurant_id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.category_id'), nullable=False)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<RestaurantCategory restcat_id=%s restaurant_id=%s category_id=%s>" % (self.restcat_id,
                                                                                       self.restaurant_id,
                                                                                       self.category_id)


class Image(db.Model):
    """Image uploaded by user for each restaurant visit."""

    __tablename__ = "images"

    image_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    visit_id = db.Column(db.Integer, db.ForeignKey('visits.visit_id'), nullable=False)
    url = db.Column(db.String(200), nullable=False)
    uploaded_At = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    taken_At = db.Column(db.DateTime, nullable=True)
    rating = db.Column(db.String(100), nullable=True)

    # Define relationship
    visit = db.relationship("Visit", backref=db.backref("images"))

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Image image_id=%s visit_id=%s>" % (self.image_id,
                                                    self.visit_id)


class Connection(db.Model):
    """Connection between two users to establish a friendship and can see each other's info."""

    __tablename__ = "connections"

    connection_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_a_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    user_b_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    status = db.Column(db.String(100), nullable=False)

    # Define relationships
    # When both columns have a relationship with the same table, need to specify how
    # to handle multiple join paths in the square brackets of foreign_keys per below
    user_a = db.relationship("User", foreign_keys=[user_a_id])
    user_b = db.relationship("User", foreign_keys=[user_b_id])

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Connection connection_id=%s first_user=%s added_user=%s status=%s>" % (self.connection_id,
                                                                                        self.user_a_id,
                                                                                        self.user_b_id,
                                                                                        self.status)


##############################################################################
# Helper functions

def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our PstgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///breadcrumbs'
    app.config['SQLALCHEMY_ECHO'] = True
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from server import app
    connect_to_db(app)
    print "Connected to DB."