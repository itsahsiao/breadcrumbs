# Yelp has provided a Python wrapper for API requests
from yelp.client import Client
from yelp.oauth1_authenticator import Oauth1Authenticator

# Import os module to get the environmental variables and secret keys
# import os

# auth = Oauth1Authenticator(
#     consumer_key=os.environ["YELP_CONSUMER_KEY"],
#     consumer_secret=os.environ["YELP_CONSUMER_SECRET"],
#     token=os.environ["YELP_TOKEN"],
#     token_secret=os.environ["YELP_TOKEN_SECRET"]
# )

# client = Client(auth)

# Yelp's provided example code for secret keys
# With this, do not need to source secrets.sh each time with new terminal
import io
import json

# read API keys
with io.open('config_secret.json') as cred:
    creds = json.load(cred)
    auth = Oauth1Authenticator(**creds)
    client = Client(auth)

# Limit API request to 20 results first
# Keep database small, until something working to make another API request
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
    print "Address: ", " ".join(business.location.display_address)
    print "Phone Number: ", business.display_phone
    print "Latitude: ", business.location.coordinate.latitude
    print "Longitude: ", business.location.coordinate.longitude
    print "Categories: "
    for category in business.categories:
        print category.name



# Might need this information for the Region Tables
# i.e. region_id = 1, city=Sunnyvale, state=CA
# City: business.location.city
# State: business.location.state_code
# Country: business.location.country_code
