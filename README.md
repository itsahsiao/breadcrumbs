BREADCRUMBS
---

<img align="center" src="/static/img/screenshots/homepage.png" width="700">

**Breadcrumbs** is a web application designed to let foodies search restaurants, track their eating history, as well as connect with friends. If you have trouble remembering what restaurants you’ve been to before, or what you’ve ordered at a restaurant that was good, then Breadcrumbs is your go-to app.

Search for restaurants by name or address. With the queried results, you can select and add a restaurant that you have visited to your own personal map, leaving behind a trail of breadcrumbs for your restaurant history. Connect with friends to see where your friends have dined at and what dishes they've tried. Breadcrumbs is a social media network built for foodies.

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

- Users can search for a restaurant by entering the name or address into the search engine at the top of the nav bar, and see all search results

### Add a restaurant visit

<img align="center" src="/static/img/screenshots/restaurant-profile.png" width="500">

- Users can add a restaurant to their restaurant history by clicking the "Leave A Breadcrumb" button on a particular restaurant's info page
- The restaurant info page also shows which of their friends have visited this particular restaurant and more

### See your own personal map for your restaurant history

<img align="center" src="/static/img/screenshots/user-profile.png" width="500">

- Users can access their profile page (and other users' as well) to see their restaurant history as a trail of breadcrumbs on a map and on a list

### Connect with friends

<img align="center" src="/static/img/screenshots/friends.png" width="500">

- Users can click on the Friends tab to see all their friends, any pending friend requests, and search for friends

<img align="center" src="/static/img/screenshots/friend-profile.png" width="500">

- If they are not friends already, users can send a friend request to another user by clicking on the "Add Friend button"
- If there is a request pending or if the two users are friends, the button will show the appropriate connection status between the two users

<img align="center" src="/static/img/screenshots/friend-requests.png" width="500">

- Users can see all pending friend requests that they have received and sent to accept or delete

### Responsive design (iPhone 6)

<img align="center" src="/static/img/screenshots/responsive-design.png" width="200">

- Breadcrumbs is also accessible by mobile!

## <a name="installation"></a>Installation
If you would like to run Breadcrumbs locally, please follow these instructions. Otherwise, please check out the deployed version of Breadcrumbs here: [ah-breadcrumbs.herokuapp.com](http://ah-breadcrumbs.herokuapp.com).

### Prerequisite:

Install [PostgreSQL](http://postgresapp.com) (Mac OSX).

Postgres needs to be running in order for the app to work. It is running when you see the elephant icon:

<img align="center" src="/static/img/screenshots/postgres-icon.png" width="200">

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
Unit Tests, Integration Tests, and Selenium Tests have been implemented.

Coverage is currently at 82%.

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

To perform the Selenium tests, run the following command line:

```$ python tests/seltests.py```

Note: Further tests still to be added, as the sample data needs to include connections and restaurant visits.
Also the Selenium tests should check for UI functionality once a user has been logged in.

## <a name="deployment"></a>Deployment
Breadcrumbs has been deployed. Check it out here: [ah-breadcrumbs.herokuapp.com](http://ah-breadcrumbs.herokuapp.com)

## <a name="future"></a>Looking Ahead
###Features

- Users can see a feed of friends' recent restaurant activity upon logging in
- Users can upload food pictures for each breadcrumb (restaurant visit) and leave comments
- Users can accept or reject Friend Requests and unfriend their Friends
- Users can message their Friends

###Other:

- More tests!

## <a name="authoe"></a>Author
Ashley Hsiao is a Software Engineer living in Vancouver, BC.
[Email](mailto:aiyihsiao@gmail.com) | [LinkedIn](http://linkedin.com/in/ashleyhsia0) | [Twitter](http://twitter.com/ashleyhsia0).
