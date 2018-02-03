"""Functions that are called multiple times, or require mocking
during unittesting (such as login_user)"""

from flask import session, render_template, json
from app import app, db
from app.models import Polls, Options


def login_user(email):
    """Adds a user's email to their session to track that
    they have logged into the application."""

    session['user'] = email


def render_with_user(template, **kwargs):
    """Wrapper for flask's render_template function, that
    also passes the user's email (if they logged in) to the
    templating function."""

    return render_template(template, user=session.get('user'), **kwargs)


def add_poll(title, options):
    """Adds a poll and its corresponding options to the database.
    Factored out of code due to usage in tests as well as app."""

    new_poll = Polls(title=title)
    db.session.add(new_poll)
    db.session.flush()

    option_rows = []

    for option in options:
        option_rows.append(Options(text=option, poll_id=new_poll.id))

    db.session.add_all(option_rows)

    return new_poll


def json_response(data):
    """Allows the app to return JSON data. Replacement for
    Flask.jsonify since that method uses deprecated code."""

    return app.response_class(
        response=json.dumps(data),
        status=200,
        mimetype='application/json'
    )
