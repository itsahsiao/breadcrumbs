"""Function to check the connection status between two users"""

from model import Connection
from model import db


def is_friends_or_pending(user_a_id, user_b_id):
    """Checks if user_a and user_b are friends, or if there is a pending request from user_a to user_b"""

    # Query to see if user_a and user_b are friends; returns None if false
    friends = db.session.query(Connection).filter(Connection.user_a_id == user_a_id,
                                                  Connection.user_b_id == user_b_id,
                                                  Connection.status == "Accepted").first()

    # Query to see if user_a has sent user_b a friend request; returns None if false
    pending_request = db.session.query(Connection).filter(Connection.user_a_id == user_a_id,
                                                          Connection.user_b_id == user_b_id,
                                                          Connection.status == "Requested").first()

    return friends, pending_request
