"""Stores SQLAlchemy schemas for each database table used.
Seperate tables that currently exist are Users, Polls, and Responses"""


from app import db


class Users(db.Model):  # pylint: disable-msg=R0903
    """SQLAlchemy table scheme that stores the users. Currently stores
    their email, and a hashed version of their password"""

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.Text, nullable=False)
    password = db.Column(db.Text, nullable=False)


class Polls(db.Model):  # pylint: disable-msg=R0903
    """SQLAlchemy table scheme that stores the polls. Polls are not
    currently connected to a user, and only stores a tite and a link
    to the table that stores responses."""

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text, nullable=False)
    responses = db.relationship('Responses')


class Responses(db.Model):  # pylint: disable-msg=R0903
    """SQLAlchemy table scheme that stores all the responses to
    all the polls. It stores the text assocated with the option and
    the id of the poll that it is a response for."""

    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    poll_id = db.Column(db.Integer, db.ForeignKey(Polls.id), nullable=False)
