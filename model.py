"""Models and database functions for Hackbright project (Breadcrumbs)."""

from flask_sqlalchemy import SQLAlchemy

# This is the connection to the PostgreSQL database; we're getting this through
# the Flask-SQLAlchemy helper library. On this, we can find the `session`
# object, where we do most of our interactions (like committing, etc.)

db = SQLAlchemy()


##############################################################################
# Model definitions

class User(db.Model):
    """User of Breadcrumbs website."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    first_name = db.column(db.String(100), nullable=False)
    last_name = db.column(db.String(100), nullable=False)
    city_code = db.column(db.String(10), db.ForeignKey('cities.city_code'), nullable=False)

    # Define relationship
    city = db.relationship("Cities")

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<User user_id=%s email=%s>" % (self.user_id, self.email)


class Restaurant(db.Model):
    """Restaurant on Breadcrumbs website."""

    __tablename__ = "restaurants"

    rest_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    city_code = db.column(db.String(10), db.ForeignKey('cities.city_code'), nullable=False)
    name = db.Column(db.String(150), nullable=False)
    address = db.Column(db.String(150), nullable=True)
    phone = db.Column(db.String(20), nullable=True)
    image_url = db.Column(db.String(200), nullable=True)
    latitude = db.Column(db.Integer, nullable=False)
    longitude = db.column(db.Integer, nullable=False)

    # Define relationship
    city = db.relationship("Cities")

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Restaurant rest_id=%s name=%s>" % (self.rest_id, self.name)


class Visit(db.Model):
    """User's visited/saved restaurant on Breadcrumbs website."""

    __tablename__ = "visits"

    visit_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    rest_id = db.Column(db.Integer, db.ForeignKey('restaurants.rest_id'), nullable=False)
    rating = db.Column(db.Integer, nullable=True)

    # Define relationships
    user = db.relationship("User")
    restaurant = db.relationship("Restaurant")

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Visit visit_id=%s rest_id=%s>" % (self.visit_id, self.rest_id)


### STILL NEED TO ADD CITIES, CATEGORIES, CONNECTIONS, AND IMAGES TABLES


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