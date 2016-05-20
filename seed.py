"""Utility file to seed info from Yelp API into the breadcrumbs database"""

from sqlalchemy import func

from model import User, Restaurant
from model import connect_to_db, db

from server import app

from yelp_api_call import load_restaurants


# Might not need this function, as no user data seeded into database initially
# Keep in database for now
# def set_val_user_id():
#     """Set value for the next user_id after seeding database"""

#     # Get the Max user_id in the database
#     result = db.session.query(func.max(User.user_id)).one()
#     max_id = int(result[0])

#     # Set the value for the next user_id to be max_id + 1
#     query = "SELECT setval('users_user_id_seq', :new_id)"
#     db.session.execute(query, {'new_id': max_id + 1})
#     db.session.commit()


def set_val_restaurant_id():
    """Set value for the next restaurant_id after seeding database"""

    # Get the Max restaurant_id in the database
    result = db.session.query(func.max(Restaurant.restaurant_id)).one()
    max_id = int(result[0])

    # Set the value for the next restaurant_id to be max_id + 1
    query = "SELECT setval('restaurants_restaurant_id_seq', :new_id)"
    db.session.execute(query, {'new_id': max_id + 1})
    db.session.commit()


if __name__ == "__main__":
    connect_to_db(app)

    # Configure mappers before creating tables in order for search trigger in
    # SQLAlchemy-Searchable to work properly
    db.configure_mappers()

    # In case tables haven't been created, create them
    db.create_all()

    # Import different types of data
    load_restaurants("Sunnyvale")
    # set_val_user_id()
    set_val_restaurant_id()
