BREADCRUMBS
---

<img align="center" src="/static/img/screenshots/homepage.png" width="500">

**Breadcrumbs** is a web application designed to let foodies track their restaurant and eating history and connect with friends. If you have trouble remembering what restaurants you’ve been to before, or what you’ve ordered at a restaurant that was good, then Breadcrumbs is your go-to app.

Search for restaurants by name or address. With the queried results, you can select and add a restaurant that you have visited to your own personal map, leaving behind a trail of breadcrumbs for your restaurant history. Connect with friends to see what restaurants your friends have dined at and what food they ate. Breadcrumbs is a social media network built for foodies.

Breadcrumbs is created with love, sweat, and tears by Ashley Hsiao. You can connect with Ashley by [email](mailto:aiyihsiao@gmail.com), [LinkedIn](http://linkedin.com/in/ashleyhsia0), or [Twitter](http://twitter.com/ashleyhsia0).

## Table of Contents

1. [Technologies](#technologies)
2. [Features](#features)
3. [Installation](#installation)
4. [Testing & Coverage](#testing)
5. [Deployment](#deployment)
6. [Looking Ahead](#future)
7. [Author](#author)

## <a name="technologies"></a>Technologies

**Front-end:** [HTML5](http://www.w3schools.com/html/), [CSS](http://www.w3schools.com/css/), [Bootstrap](http://getbootstrap.com), [Javascript](https://developer.mozilla.org/en-US/docs/Web/JavaScript), [jQuery](https://jquery.com/), [AJAX](http://api.jquery.com/jquery.ajax/)

**Back-end:** [Python](https://www.python.org/), [Flask](http://flask.pocoo.org/), [Jinja2](http://jinja.pocoo.org/docs/dev/), [PostgreSQL](http://www.postgresql.org/), [SQLAlchemy](http://www.sqlalchemy.org/)

**Libraries:** [SQLAlchemy-Searchable](https://sqlalchemy-searchable.readthedocs.io)

**APIs:** [Yelp](https://www.yelp.ca/developers/documentation/v2/overview), [Google Maps](https://developers.google.com/maps/)

## <a name="features"></a>Features
### Search for a restaurant

<img align="center" src="/static/img/screenshots/search-restaurants.png" width="500">

### Add a restaurant visit

<img align="center" src="/static/img/screenshots/restaurant-profile.png" width="500">

### See your own personal map for your restaurant history

<img align="center" src="/static/img/screenshots/user-profile.png" width="500">

### Connect with friends

<img align="center" src="/static/img/screenshots/friends.png" width="500">

<img align="center" src="/static/img/screenshots/friend-profile.png" width="500">

<img align="center" src="/static/img/screenshots/friend-requests.png" width="500">

### Responsive design (iPhone 6)

<img align="center" src="/static/img/screenshots/responsive-design.png" width="200">

## <a name="installation"></a>Installation
As Breadcrumbs has not yet been deployed, please follow these instructions to run Breadcrumbs locally on your machine:

### Prerequisite:

Install [PostgreSQL](http://postgresapp.com) (Mac OSX).

Postgres needs to be running in order for the app to work. It is running when you see the elephant icon:

<img align="center" src="/static/img/screenshots/postgres-icon.png">

Add /bin directory to your path to use PostgreSQL commands and install the Python library.

Use Sublime to edit `~/.bash_profile` or `~/.profile`, and add:

```export PATH=/Applications/Postgres.app/Contents/Versions/9.5/bin/:$PATH``` 

### Set up Breadcrumbs:

Clone this repository:

```$ git clone https://github.com/ashleyhsia0/breadcrumbs.git```

Create a virtual environment and activate it:

```
$ virtualenv env
$ source env/bin/activate
```

Install the dependencies:

```$ pip install -r requirements.txt```

Get an API key from Yelp and store in a secrets.sh or use a JSON per the Yelp API documentation, but make sure to put the file in your `.gitignore`.

Run PostgreSQL (make sure elephant icon is active).

Create database with the name `breadcrumbs`.

```$ createdb breadcrumbs```

Seed the database with restaurants:

```$ python seed.py```

Finally, to run the app, start the server:

```$ python server.py```

Go to `localhost:5000` in your browser to start using Breadcrumbs!

## <a name="testing"></a>Testing & Coverage
UnitTests and IntegrationTests have been implemented.

Currently the coverage is 55%.

<img align="center" src="/static/img/screenshots/testing-coverage.png" width="500">

To run tests, run the following command line:

```$ coverage run --omit=env/* tests/tests.py```

To get a coverage report, run the following:

```$ coverage report -m```

For an HTML version of the report, run the running:

```
$ coverage html
$ open htmlcov/index.html
```

## <a name="deployment"></a>Deployment
Deployment details coming very soon!

## <a name="future"></a>Looking Ahead
###Features

- Users can see a feed of friends' recent restaurant activity upon logging in
- Users can upload food pictures for each breadcrumb (restaurant visit) and leave comments
- Users can accept or reject Friend Requests and unfriend their Friends
- Users can message their Friends

###Other:

- Deployment
- IntegrationTesting, Selenium Testing

## <a name="authoe"></a>Author
Ashley Hsiao is a Software Engineer living in the San Francisco Bay Area.
[Email](mailto:aiyihsiao@gmail.com) | [LinkedIn](http://linkedin.com/in/ashleyhsia0) | [Twitter](http://twitter.com/ashleyhsia0).