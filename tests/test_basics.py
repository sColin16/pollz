"""Basic (and currently only) test module for the pollz application."""

import os
import sys
import unittest
from unittest.mock import MagicMock
from passlib.hash import sha256_crypt
from flask import json

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
os.environ['APP_MODE'] = 'test'

from app import app, db, routes  # pylint:disable=unused-import, wrong-import-position
from app.models import Users, Polls, Options  # pylint:disable=wrong-import-position
from app.helpers import add_poll  # pylint:disable=wrong-import-position

TEST_EMAIL = 'test@test.com'
TEST_PASSWORD = 'mypassword'
TEST_POLL_TITLE = 'Test poll'
TEST_POLL_OPTIONS = ['Option A', 'Option B']


def clear_users():
    """Clears the database of all users, for use when an empty
    database is necessary for a test to ensure its passing."""

    db.session.query(Users).delete()
    db.session.commit()


def clear_polls():
    """Clears the database of all polls, in case the uniqueness
    of a poll during testing is important (not used yet)."""

    db.session.query(Polls).delete()
    db.session.query(Options).delete()
    db.session.commit()


def manual_register(email=TEST_EMAIL, password=TEST_PASSWORD):
    """Manually add a user to the database, to pass over the
    register route of the app. This allows tests to run faster,
    prevents testing more than one part of the code, and eliminates
    problems with testing login simply."""

    new_user = Users(email=email, password=password)
    db.session.add(new_user)


def manual_create_poll(title=TEST_POLL_TITLE, options=None):
    """Manually adds a poll to the database, for similar reasons
    in implementing a manual_register function."""

    if options is None:
        options = TEST_POLL_OPTIONS

    return add_poll(title, options)


def manual_vote(poll_id, option, change=1):
    """Manually modifies an option's vote count. Avoids the need
    to submit unnecessary requests to the server."""

    poll = Polls.query.join(Options).filter(Polls.id == poll_id).first()

    poll.options[option].votes = poll.options[option].votes + change


class BaseTestClass(unittest.TestCase):
    """A general purpose testcase that creates an app test instance,
    and the database. Also runs most basic tests"""

    def __init__(self, *args, **kwargs):
        """Instantiates necessary variables, and performs mocks to set
        up variables for the unit tests."""

        super(BaseTestClass, self).__init__(*args, **kwargs)
        self.client = app.test_client()
        db.create_all()

    def shortDescription(self):
        """Prevents printing the doc string during testing"""

        return None

    def register(self, email=TEST_EMAIL, password=TEST_PASSWORD):
        """Helper function that uses the apps register route to
        register a new user, and log them in (as is done by default).
        Needed for both LoginTests and PollTests, since registration
        is required for creating polls"""

        response = self.client.post(
            '/register',
            data=dict(email=email, password=password),
            follow_redirects=True
        )

        return response


class LoginTests(BaseTestClass):
    """Test Case that handles tests related to login and registration"""

    def __init__(self, *args, **kwargs):
        """Sets up additional mocks so that password hashing (which
        is slow) does not have to be run"""

        super(LoginTests, self).__init__(*args, **kwargs)

        sha256_crypt.encrypt = MagicMock(side_effect=lambda password: password)
        sha256_crypt.verify = MagicMock(side_effect=lambda password, hash: password == hash)

    def tearDown(self):
        """Function run by unittest module after every individual test."""
        self.logout()

    def login(self, email=TEST_EMAIL, password=TEST_PASSWORD):
        """Helper function that uses the app's login route to test login functionality."""

        return self.client.post(
            '/login',
            data=dict(email=email, password=password),
            follow_redirects=True
        )

    def logout(self):
        """Follows the app's logout route to log the user out."""

        return self.client.get(
            '/logout',
            follow_redirects=True
        )

    def test_index_up(self):
        """Basic test that ensures that the basic functions of the
        app are functioning."""

        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_valid_registration(self):
        """Ensures that a registering user whose email has not been used yet
        is properly proceseed by the register route."""

        clear_users()
        response = self.register()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Users.query.filter_by(email=TEST_EMAIL).count(), 1)

    def test_invalid_registration(self):
        """Ensures that no duplicate users register through the app's register route."""

        clear_users()
        manual_register()
        response = self.register()
        self.assertIn(b'That email has already been used to register', response.data)

    def test_valid_login(self):
        """Tests that a registered user with a valid email and password
        can log into the app."""

        manual_register()
        response = self.login()
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Dashboard', response.data)

    def test_invalid_login_email(self):
        """Ensures that a user who enters a valid password, but an invalid email will
        not gain access to the application."""

        manual_register()
        response = self.login('bademail@test.com', TEST_PASSWORD)
        self.assertIn(b'Incorrect email or password', response.data)

    def test_invalid_login_password(self):
        """Ensures that a user who enter a valid email, but an invalid password will
        also not gain access to the application."""

        manual_register()
        response = self.login(TEST_EMAIL, 'badpassword')
        self.assertIn(b'Incorrect email or password', response.data)

    def test_valid_logout(self):
        """Ensures the logout functionality works as expected."""

        self.register()
        response = self.logout()
        self.assertEqual(response.status_code, 200)

    def test_invalid_logout(self):
        """Ensures that a logged out user that gains access to the
        logout route will cause the application to crash."""

        response = self.logout()
        self.assertEqual(response.status_code, 200)

    def test_login_invalidated(self):
        """Tests that a user who is not logged in cannot gain access
        to the dashboard route, or other routes that require login."""

        response = self.client.get('/dashboard')
        self.assertEqual(response.status_code, 302)

    def test_login_forbidden(self):
        """Tests that a user who is logged in cannot access routes such
        as login or register, that forbid a logged in user."""

        self.register()
        response = self.client.get('/register')
        self.assertEqual(response.status_code, 302)


class PollTests(BaseTestClass):
    """Test Case that handles tests related to poll creation and voting"""

    def create_poll(self, title=TEST_POLL_TITLE, options=None):
        """Helper function that submits data to test the app's
        create poll route."""

        if options is None:
            options = TEST_POLL_OPTIONS

        return self.client.post(
            '/create',
            data={'title': title, 'options[]': options},
            follow_redirects=True
        )

    def vote(self, poll_id, option, previous_option, method):
        """Submits a vote to the server using the specified method"""

        return self.client.get(
            'vote?poll_id={}&option={}&previous_option={}&method={}'
            .format(poll_id, option, previous_option, method),
            follow_redirects=True
        )

    def test_create_poll(self):
        """Ensures that a user who submits the form via the create route
        will allow them to create a poll as expected."""

        clear_users()
        self.register()
        response = self.create_poll()
        self.assertIn(b"Poll created", response.data)

    def test_view_poll(self):
        """Ensures that a poll added to the database can be properly
        viewed via the view route. This primarily tests that the join
        between the Polls and Responses table functions correctly."""

        manual_create_poll()
        response = self.client.get('/view')
        self.assertIn(bytes(TEST_POLL_TITLE, 'utf-8'), response.data)
        self.assertIn(bytes(TEST_POLL_OPTIONS[0], 'utf-8'), response.data)
        self.assertIn(bytes(TEST_POLL_OPTIONS[1], 'utf-8'), response.data)

    def test_vote_add(self):
        """Ensures that the app's 'add' method for submitting votes
        functions as expected. Does not test front-end verfication."""

        poll = manual_create_poll()

        response = self.vote(poll.id, 0, None, 'add')
        json_data = json.loads(str(response.data, 'utf-8'))
        voted_option = json_data[0].get('votes')
        empty_option = json_data[1].get('votes')

        self.assertEqual(voted_option, 1)
        self.assertEqual(empty_option, 0)

    def test_vote_change(self):
        """Ensure that the app's 'change' method for submitting votes
        function as expected, decrementing the appropraite vote count.
        Does not test front-end verification."""

        poll = manual_create_poll()
        manual_vote(poll.id, 0)

        response = self.vote(poll.id, 1, 0, 'change')
        json_data = json.loads(str(response.data, 'utf-8'))
        changed_option = json_data[0].get('votes')
        voted_option = json_data[1].get('votes')

        self.assertEqual(changed_option, 0)
        self.assertEqual(voted_option, 1)

    def test_vote_remove(self):
        """Ensures that the app's 'remove method for cancelling a vote
        functions as expected, decremineting the specified option's vote
        count. Does not test front-end verification."""

        poll = manual_create_poll()
        manual_vote(poll.id, 0)

        response = self.vote(poll.id, 0, None, 'remove')
        json_data = json.loads(str(response.data, 'utf-8'))
        removed_option = json_data[0].get('votes')
        empty_option = json_data[1].get('votes')

        self.assertEqual(removed_option, 0)
        self.assertEqual(empty_option, 0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
