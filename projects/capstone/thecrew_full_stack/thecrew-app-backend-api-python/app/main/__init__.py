"""Main blueprint responsible for displaying web pages."""

__author__ = "Filipe Bezerra de Sousa"

from flask import Blueprint

bp = Blueprint('main', __name__)

from . import routes  # noqa: E402
