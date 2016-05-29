"""Functions for the connection/relationship between users"""

from model import Connection, User
from model import db


def is_friends_or_pending(user_a_id, user_b_id):
    """
    Checks the friend status between user_a and user_b.

    Checks if user_a and user_b are friends.
    Checks if there is a pending friend request from user_a to user_b.
    """

    # Query to see if user_a and user_b are friends; returns None if false
    is_friends = db.session.query(Connection).filter(Connection.user_a_id == user_a_id,
                                                     Connection.user_b_id == user_b_id,
                                                     Connection.status == "Accepted").first()

    # Query to see if user_a has sent user_b a friend request which is pending; returns None if false
    is_pending = db.session.query(Connection).filter(Connection.user_a_id == user_a_id,
                                                     Connection.user_b_id == user_b_id,
                                                     Connection.status == "Requested").first()

    return is_friends, is_pending


def get_friend_requests(user_id):
    """
    Get user's friend requests.

    Returns users that user received friend requests from.
    Returns users that user sent friend requests to.
    """

    # Query to get all users that user received friend requests from
    received_friend_requests = db.session.query(User).filter(
        Connection.user_b_id == user_id,
        Connection.status == "Requested").join(
        Connection,
        Connection.user_a_id == User.user_id).all()

    # Note from mentor: Can break line from parentheses for styling

    # Query to get all users that user sent friend quests to
    sent_friend_requests = db.session.query(User).filter(Connection.user_a_id == user_id,
                                                         Connection.status == "Requested").join(Connection,
                                                                                                Connection.user_b_id == User.user_id).all()

    return received_friend_requests, sent_friend_requests


def get_friends(user_id):
    """
    Return a query for user's friends

    Note: This does not return User objects, just the query
    """

    # Query to get all friends for user
    friends = db.session.query(User).filter(Connection.user_a_id == user_id,
                                            Connection.status == "Accepted").join(Connection,
                                                                                  Connection.user_b_id == User.user_id)

    return friends
