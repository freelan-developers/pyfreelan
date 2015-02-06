"""
A user class, as required by flask_login.
"""

from flask.ext.login import UserMixin


class User(UserMixin):
    """
    Represents a user.
    """

    def __init__(self, username):
        """
        Initialize a user.

        :param username: The username.
        """
        super(User, self).__init__()

        self.username = username

    def get_id(self):
        return unicode(self.username)
