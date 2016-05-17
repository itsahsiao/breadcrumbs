"""Utility file to seed info from Yelp API into the breadcrumbs database"""

from sqlalchemy import func

from test_search_model import City, Restaurant
from test_search_model import connect_to_db, db
# from model import City, Restaurant
# from model import connect_to_db, db

from server import app

# Yelp has provided a Python wrapper for API requests
# Import these as indicated per Yelp documentation
from yelp.client import Client
from yelp.oauth1_authenticator import Oauth1Authenticator

# Keep Yelp API secret keys in json file per Yelp documentation
import io
import json


def load_restaurants(city):
    """Load restaurants from Yelp API into database."""

    print "Restaurants"

    # Delete all rows in table, so if we need to run this a second time,
    # we won't be trying to add duplicate users
    Restaurant.query.delete()

    # Read Yelp API keys
    with io.open('config_secret.json') as cred:
        creds = json.load(cred)
        auth = Oauth1Authenticator(**creds)
        client = Client(auth)

    ## TO-DO:
    # Limit / offset to get all results for a restaurant
    # Separate seed.py from help function

    # Set search parameters for Yelp API request
    # Limit API request to 20 results first
    # Keep database small, until something working to make another API request
    params = {
        'term': 'food',
        'limit': 20,
    }

    # Make Yelp API request and store response
    response = client.search(city, **params)

    # Check to see if city exists in database to get the city id
    # If not, add city into database and get city it
    if db.session.query(City.city_id).filter(City.name == city).first():
        city_id = db.session.query(City.city_id).filter(City.name == city).first()
        city_id = city_id[0]
    else:
        new_city = City(name=city)
        db.session.add(new_city)
        db.session.commit()
        city_id = new_city.city_id

    # API response returns a SearchResponse object
    # Specify information by looking at its attributes and indexing
    # response.businesses returns a list of business objects with further attributes
    for business in response.businesses:
        restaurant = Restaurant(city_id=city_id,
                                name=business.name,
                                address=" ".join(business.location.display_address),
                                phone=business.display_phone,
                                image_url=business.image_url,
                                latitude=business.location.coordinate.latitude,
                                longitude=business.location.coordinate.longitude)

        # Add to the session to store into the db
        db.session.add(restaurant)

        # Commit to save changes
        db.session.commit()   



# This makes a runtime error
# Cannot do API request outside of the function???

# def load_restaurants(business, city):
#     """Load restaurants from Yelp API into database."""

#     print "Restaurants"

#     # Delete all rows in table, so if we need to run this a second time,
#     # we won't be trying to add duplicate users
#     Restaurant.query.delete()

#     # Check to see if city exists in database to get the city id
#     # If not, add city into database and get city it
#     if db.session.query(City.city_id).filter(City.name == city).first() != None:
#         city_id = db.session.query(City.city_id).filter(City.name == city).first()
#         city_id = city_id[0]
#     else:
#         city = City(name=city)
#         db.session.add(city)
#         db.session.commit()
#         city_id = city.city_id

#     restaurant = Restaurant(city_id=city_id,
#                             rest_name=business.name,
#                             address=" ".join(business.location.display_address),
#                             phone=business.display_phone,
#                             image_url=business.image_url,
#                             latitude=business.location.coordinate.latitude,
#                             longitude=business.location.coordinate.longitude)

#     # Add to the session to store into the db
#     db.session.add(restaurant)

#     # Commit to save changes
#     db.session.commit()


# # Read Yelp API keys
# with io.open('config_secret.json') as cred:
#     creds = json.load(cred)
#     auth = Oauth1Authenticator(**creds)
#     client = Client(auth)

# # Set search parameters for Yelp API request
# # Limit API request to 20 results first
# # Keep database small, until something working to make another API request
# params = {
#     'term': 'food',
#     'limit': 20,
# }

# # Set city here when grabbing restaurant info from Yelp by city
# city = "Sunnyvale"

# # Make Yelp API request and store response
# response = client.search(city, **params)

# # API response returns a SearchResponse object
# # Specify information by looking at its attributes and indexing
# # response.businesses returns a list of business objects with further attributes
# for business in response.businesses:
#     load_restaurants(business, city)




if __name__ == "__main__":
    connect_to_db(app)

    # In case tables haven't been created, create them
    db.create_all()

    # Import different types of data
    # load_restaurants()
    # load_categories()
    # load_ratings()
    # set_val_user_id()