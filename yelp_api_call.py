"""Functions to make API call to Yelp for restaurants in a city"""

from model import City, Restaurant
from model import db

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
        existing_city = db.session.query(City).filter(City.name == city).one()

    except NoResultFound:
        new_city = City(name=city)
        db.session.add(new_city)
        db.session.commit()
        return new_city.city_id

    return existing_city.city_id


# Resource for how to offset Yelp API results from http://www.mfumagalli.com/wp/portfolio/nycbars/
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

    # Get city id, as city id is a required parameter when adding a restaurant to the database
    city_id = get_city_id(city)

    # Start offset at 0 to return the first 20 results from Yelp API request
    offset = 0

    # Get total number of restaurants for this city
    total_results = get_restaurants(city, offset).total

    # Get all restaurants for a city and load each restaurant into the database
    # Note: Yelp has a limitation of 1000 for accessible results, so get total results
    # if less than 1000 or get only 1000 results back even if there should be more
    while 1000 > offset < total_results:

        # API response returns a SearchResponse object with accessible attributes
        # response.businesses returns a list of business objects with further attributes
        for business in get_restaurants(city, offset).businesses:
            restaurant = Restaurant(city_id=city_id,
                                    name=business.name,
                                    address=" ".join(business.location.display_address),
                                    phone=business.display_phone,
                                    image_url=business.image_url,
                                    latitude=business.location.coordinate.latitude,
                                    longitude=business.location.coordinate.longitude)

            # Add each restaurant to the db
            db.session.add(restaurant)

        # Yelp returns only 20 results each time, so need to offset by 20 while iterating
        offset += 20

    # Commit to save changes
    db.session.commit()
