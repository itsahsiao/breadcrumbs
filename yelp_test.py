# Yelp has provided a Python wrapper for API requests
from yelp.client import Client
from yelp.oauth1_authenticator import Oauth1Authenticator

# Import os module to get the environmental variables and secret keys
import os

auth = Oauth1Authenticator(
    consumer_key=os.environ["YELP_CONSUMER_KEY"],
    consumer_secret=os.environ["YELP_CONSUMER_SECRET"],
    token=os.environ["YELP_TOKEN"],
    token_secret=os.environ["YELP_TOKEN_SECRET"]
)

client = Client(auth)

# Limit API request by 20 results first
params = {
    'term': 'food',
    'limit': 20,
}

response = client.search('Sunnyvale', **params)

# API response returns a SearchResponse object
# Specify information by looking at its attributes and indexing

for business in response.businesses:
    print "------RESTAURANT----------"
    print "Business Name: ", business.name
    print "Business Image: ", business.image_url
    print "Address: ", business.location.display_address
    print "Phone Number: ", business.display_phone
    print "Latitude: ", business.location.coordinate.latitude
    print "Longitude: ", business.location.coordinate.longitude



# Might need this information for the Region Tables
# i.e. region_id = 1, city=Sunnyvale, state=CA
City: business.location.city
State: business.location.state_code

    print "Categories: ", business.categories.name




# for business in response.businesses:
#     print business.name, business.url, business.id

# print response.businesses[0].id

# client.get_business(response.businesses[0].id)


