"""Basic (and currently only) test module for the pollz application."""

import os
import sys
import unittest
from unittest.mock import MagicMock
from passlib.hash import sha256_crypt

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
os.environ['APP_MODE'] = 'test'

from app import app, db, routes  # pylint:disable=unused-import, wrong-import-position
from app.models import Users, Polls, Responses  # pylint:disable=wrong-import-position

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
    db.session.query(Responses).delete()
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

    new_poll = Polls(title=title)
    db.session.add(new_poll)
    db.session.flush()

    option_a_row = Responses(text=options[0], poll_id=new_poll.id)
    option_b_row = Responses(text=options[1], poll_id=new_poll.id)

    db.session.add_all([option_a_row, option_b_row])


class BasicTests(unittest.TestCase):
    """Unittest testcase that handles all basic tests cases
    (which, right now, really means every test)"""

    def __init__(self, *args, **kwargs):
        """Instantiates necessary variables, and performs mocks to set
        up variables for the unit tests."""

        super(BasicTests, self).__init__(*args, **kwargs)
        self.client = app.test_client()
        db.create_all()

        sha256_crypt.encrypt = MagicMock(side_effect=lambda password: password)
        sha256_crypt.verify = MagicMock(side_effect=lambda password, hash: password == hash)

    def setUp(self):
        """Function run by the unittest module before every individual test."""
        pass

    def tearDown(self):
        """Function run by unittest module after every individual test."""

        self.logout()

    def register(self, email=TEST_EMAIL, password=TEST_PASSWORD):
        """Helper function that uses the apps register route to
        register a new user, and log them in (as is done by default)."""

        return self.client.post(
            '/register',
            data=dict(email=email, password=password),
            follow_redirects=True
        )

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

    def create_poll(self, title=TEST_POLL_TITLE, options=None):
        """Helper function that submits data to test the app's
        create poll route."""

        if options is None:
            options = TEST_POLL_OPTIONS

        return self.client.post(
            '/create',
            data=dict(title=title, optionA=options[0],
                      optionB=options[1]),
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
        self.assertIn(b'That email has already been used to register',
                      response.data)

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

    def test_create_poll(self):
        """Ensures that a user who submits the form via the create route
        will allow them to create a poll as expected."""

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


if __name__ == "__main__":
    unittest.main()
