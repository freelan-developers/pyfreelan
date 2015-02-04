"""
Exceptions.
"""

from flask import jsonify


class UnexpectedFormat(Exception):
    """
    The request received data in an unexpected format and does not like it very
    much.
    """
    status_code = 406

    def __init__(self, message):
        super(UnexpectedFormat, self).__init__()
        self.message = message

    def to_dict(self):
        return {
            'message': self.message,
        }

    def to_response(self):
        response = jsonify(self.to_dict())
        response.status_code = self.status_code
        return response
