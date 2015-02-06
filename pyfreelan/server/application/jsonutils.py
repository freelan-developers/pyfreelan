"""
JSON-related functions.
"""

import json

from flask.json import JSONEncoder
from datetime import datetime


class ISODateJSONEncoder(JSONEncoder):
    def default(self, obj):
        """
        Convert an object to its JSON representation.

        :param obj: The object to convert.
        :returns: The JSON string representation.

        >>> ISODateJSONEncoder().default({'a': 37})
        '{"a": 37}'

        >>> ISODateJSONEncoder().default(None)
        'null'

        >>> ISODateJSONEncoder().default(42)
        '42'

        >>> ISODateJSONEncoder().default(0.42)
        '0.42'

        >>> ISODateJSONEncoder().default('hello world')
        '"hello world"'

        >>> ISODateJSONEncoder().default([1, 2])
        '[1, 2]'

        >>> ISODateJSONEncoder().default(datetime(2015, 3, 10, 10, 45, 37, 38))
        '2015-03-10T10:45:37.000038'
        """
        if isinstance(obj, datetime):
            return obj.isoformat()

        return json.dumps(obj)
