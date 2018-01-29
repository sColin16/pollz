"""Functions that are called multiple times, or require mocking
during unittesting (such as login_user)"""


from flask import session, render_template


def login_user(email):
    """Adds a user's email to their session to track that
    they have logged into the application."""

    session['user'] = email


def render_with_user(template, **kwargs):
    """Wrapper for flask's render_template function, that
    also passes the user's email (if they logged in) to the
    templating function."""

    return render_template(template, user=session.get('user'), **kwargs)
