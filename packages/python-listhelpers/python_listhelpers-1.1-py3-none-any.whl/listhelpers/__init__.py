"""
    list
    ~~~~~~~~~~~~~

    A set of various list helpers.

    :copyright: (c) 2016 by Dusty Gamble.
    :license: MIT, see LICENSE for more details.
"""

__version__ = '1.1'



def listify(obj):
    # Because None is used for specific functionality, preserve it.
    if obj is None:
        return None

    try:
        assert type(obj) is not str
        assert hasattr(obj, '__iter__')
    except AssertionError:
        obj = [obj, ]

    return obj
