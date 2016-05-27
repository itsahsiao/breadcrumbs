"""Functions that define the connection/relationship between users"""

from model import Connection, User
from model import db


def is_friends_or_pending(user_a_id, user_b_id):
    """Checks if user_a and user_b are friends, or if there is a pending request from user_a to user_b"""

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
    """Get all received and sent friend requests for a user"""

    # Query to get all friend requests received
    received_friend_requests = db.session.query(User).filter(Connection.user_b_id == user_id,
                                                             Connection.status == "Requested").join(Connection,
                                                                                                    Connection.user_a_id == User.user_id).all()

    # Query to get all friend requests sent
    sent_friend_requests = db.session.query(User).filter(Connection.user_a_id == user_id,
                                                         Connection.status == "Requested").join(Connection,
                                                                                                Connection.user_b_id == User.user_id).all()

    return received_friend_requests, sent_friend_requests


def get_friends(user_id):
    """Get user's friends"""

    # Query to get all friends for current user
    friends = db.session.query(User).filter(Connection.user_a_id == user_id,
                                            Connection.status == "Accepted").join(Connection,
                                                                                  Connection.user_b_id == User.user_id).all()

    return friends
