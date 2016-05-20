"""Utility file to seed info from Yelp API into the breadcrumbs database"""

from sqlalchemy import func

from model import City, User, Restaurant
from model import connect_to_db, db

from server import app

# Import SQLALchemy exception for try/except
from sqlalchemy.orm.exc import NoResultFound

# Yelp has provided a Python wrapper for API requests
# Import these as indicated per Yelp documentation
from yelp.client import Client
from yelp.oauth1_authenticator import Oauth1Authenticator

# Keep Yelp API secret keys in json file per Yelp documentation
import io
import json


def get_city_id(city):
    """Get the city id from database. Otherwise, add city to database and get the city id."""

    # Check if argument (city) passed in is a city that exists in the database
    # If not, instantiate the new city in the database and get the city id
    # Otherwise, return the city id for the existing city from the database
    try:
        # existing_city_id = db.session.query(City.city_id).filter(City.name == city).one()[0]
        existing_city = db.session.query(City).filter(City.name == city).one()
        # TODO: Ask if object better or tuple better???

    except NoResultFound:
        new_city = City(name=city)
        db.session.add(new_city)
        db.session.commit()
        return new_city.city_id

    return existing_city.city_id


# Got ideas on how to offset Yelp API results from http://www.mfumagalli.com/wp/portfolio/nycbars/
def get_restaurants(city, offset):
    """
    Make API request to Yelp to get restaurants for a city, and offset the results by an amount.

    Note that Yelp only returns 20 results each time, which is why we need to offset if we want
    the next Nth results.
    """

    # Read Yelp API keys
    with io.open('config_secret.json') as cred:
        creds = json.load(cred)
        auth = Oauth1Authenticator(**creds)
        client = Client(auth)

    # Set search parameters for Yelp API request
    # Set term as restaurant to get restaurants back as the results
    # Also pass in offset, so Yelp knows how much to offset by
    params = {
        'term': 'restaurant',
        'offset': offset
    }

    # Make Yelp API call and return the API response
    return client.search(city, **params)


def load_restaurants(city):
    """Get all restaurants for a city from Yelp and load restaurants into database."""

    # Delete all rows in table, so if we need to run this a second time,
    # we won't be trying to add duplicate users
    Restaurant.query.delete()

    # Get city id, as city id is a required parameter when adding a restaurant to the database
    city_id = get_city_id(city)

    # Start offset at 0 to return the first 20 results from Yelp API request
    offset = 0
    response = get_restaurants(city, offset)

    # Get total number of restaurants for this city
    total_results = response.total

    # Offset by 20 each time to get all restaurants and load each restaurant into the database
    # while offset < total_results:
    # Return 100 results for now, as Yelp has a limitation for accessible results (1000)
    # TODO: Ask in help queue re: Yelp limitation and dataset
    for i in range(0, 100, 20):

        for business in response.businesses:
            restaurant = Restaurant(city_id=city_id,
                                    name=business.name,
                                    address=" ".join(business.location.display_address),
                                    phone=business.display_phone,
                                    image_url=business.image_url,
                                    latitude=business.location.coordinate.latitude,
                                    longitude=business.location.coordinate.longitude)

            # Add each restaurant to the db
            db.session.add(restaurant)

        offset += 20

        response = get_restaurants(city, offset)

    # Commit to save changes
    db.session.commit()


    ### BELOW CODE WAS PREVIOUS THOUGHT PROCESS - KEEP FOR NOW ###

    # city_id = get_city_id(city)

    # offset = 0

    # response = get_restaurants(city, offset)

    # # total_results = response.total

    # # Test with 40 instead of total_results first to see if working
    # for i in range(0, 40, 20):

    #     for business in response.businesses:
    #         restaurant = Restaurant(city_id=city_id,
    #                                 name=business.name,
    #                                 address=" ".join(business.location.display_address),
    #                                 phone=business.display_phone,
    #                                 image_url=business.image_url,
    #                                 latitude=business.location.coordinate.latitude,
    #                                 longitude=business.location.coordinate.longitude)

    #         # Add to the session to store into the db
    #         db.session.add(restaurant)

    #     offset += 20

    #     response = get_restaurants(city, offset)

    #     # Commit to save changes
    #     db.session.commit()


# def load_restaurants(city):
#     """Load restaurants from Yelp API into database."""

#     print "Restaurants"

#     # Delete all rows in table, so if we need to run this a second time,
#     # we won't be trying to add duplicate users
#     Restaurant.query.delete()

#     # Read Yelp API keys
#     with io.open('config_secret.json') as cred:
#         creds = json.load(cred)
#         auth = Oauth1Authenticator(**creds)
#         client = Client(auth)

#     ## TO-DO:
#     # Limit / offset to get all results for a restaurant
#     # Separate seed.py from help function

#     # Set search parameters for Yelp API request
#     # Limit API request to 20 results first
#     # Keep database small, until something working to make another API request
#     params = {
#         'term': 'food',
#         'limit': 20,
#     }

#     # Make Yelp API request and store response
#     response = client.search(city, **params)

#     # Check to see if city exists in database to get the city id
#     # If not, add city into database and get city it
#     if db.session.query(City.city_id).filter(City.name == city).first():
#         city_id = db.session.query(City.city_id).filter(City.name == city).first()
#         city_id = city_id[0]
#     else:
#         new_city = City(name=city)
#         db.session.add(new_city)
#         db.session.commit()
#         city_id = new_city.city_id

#     # API response returns a SearchResponse object
#     # Specify information by looking at its attributes and indexing
#     # response.businesses returns a list of business objects with further attributes
#     for business in response.businesses:
#         restaurant = Restaurant(city_id=city_id,
#                                 name=business.name,
#                                 address=" ".join(business.location.display_address),
#                                 phone=business.display_phone,
#                                 image_url=business.image_url,
#                                 latitude=business.location.coordinate.latitude,
#                                 longitude=business.location.coordinate.longitude)

#         # Add to the session to store into the db
#         db.session.add(restaurant)

#         # Commit to save changes
#         db.session.commit()


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
    # load_categories()
    # set_val_user_id()
    set_val_restaurant_id()