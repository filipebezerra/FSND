"""TheCrew API Backend.

The TheCrew is a Casting Agency company that is responsible for creating movies 
and managing and assigning actors to those movies.

So TheCrew API is the backend application that serves and accepts JSON data for 
our applications and third-party applications.

The code follows [PEP 8 style guide](https://pep8.org/).
"""

__author__ = "Filipe Bezerra de Sousa"

from flask_migrate import upgrade
from app import create_app, db
from app.models import Movie, Actor, Gender, movies_actors

app = create_app()


@app.shell_context_processor
def make_shell_context():
    return {
        'db': db,
        'Movie': Movie,
        'Actor': Actor,
        'Gender': Gender,
        'movies_actors': movies_actors
    }


@app.cli.command()
def deploy():
    """Run deployment tasks."""
    # Migrate database to latest version
    upgrade()
    # Create or update genders
    Gender.insert_genders()


if __name__ == '__main__':
    app.run(
        use_reloader=False,
        use_debugger=False,
        passthrough_errors=True,
        host='0.0.0.0')
