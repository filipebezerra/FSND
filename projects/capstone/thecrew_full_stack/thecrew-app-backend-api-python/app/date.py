"""Utilities for using date objects.

    now(): the main function exported by this module.
"""

__author__ = "Filipe Bezerra de Sousa"

from datetime import datetime, timezone
from flask import current_app


def date_to_str(date):
    """Convert a date object to a string representation using the application 
    date format.

    :param date: The :class:`datetime.datetime` object. 
    :return: The date string or `None` if can't convert it.
    """
    try:
        date_string = date.strftime(current_app.config['THECREW_DATE_FORMAT'])
    except (TypeError, AttributeError):
        return None
    return date_string


def str_to_date(date_string):
    """Convert back string representation of a date to the date object using 
    the application date format.
    
    :param date_string: The string representation of a :class:`datetime.datetime` 
    object.
    :return: A instance of a :class:`datetime.datetime` object or `None` if 
    can't convert it.
    """
    try:
        date = datetime.strptime(
            date_string, current_app.config['THECREW_DATE_FORMAT'])
    except ValueError:
        return None
    return date


def now():
    """A instance of :class:`datetime.datetime` object with utc time zone info.

    :return: A instance of a :class:`datetime.datetime` object.
    """
    return datetime.now(tz=timezone.utc)
