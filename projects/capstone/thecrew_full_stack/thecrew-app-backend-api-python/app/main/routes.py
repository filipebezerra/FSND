"""Route decorators responsible for routing URLs to the appropriate web page."""

__author__ = "Filipe Bezerra de Sousa"

from flask import redirect, render_template
from app.main import bp
from app.integrations.auth0 import build_authorize_url


@bp.route('/login', methods=['GET'])
@bp.route('/signup', methods=['GET'])
def login():
    """Redirect to the login/signup web page."""
    return redirect(build_authorize_url())


@bp.route('/', methods=['GET'])
@bp.route('/welcome', methods=['GET'])
def welcome_callback():
    """Render the welcome web page."""
    return render_template('welcome.html', title='TheCrew Casting Agency')
