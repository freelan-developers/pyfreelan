"""
The Flask application.
"""

from flask import Flask

APP = Flask('pyfreelan')

@APP.route('/')
def index():
    return "lol"
