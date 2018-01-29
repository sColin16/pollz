# TODO: prepopulate db with some users and polls, clear
# polls/users must add them back, or do something else

import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
os.environ['APP_MODE'] = 'test'

import unittest
from unittest.mock import MagicMock, patch
from app import app, db, routes
from app.models import Users, Polls, Responses
from passlib.hash import sha256_crypt


def clear_users():
    db.session.query(Users).delete()
    db.session.commit()


def clear_polls():
    db.session.query(Polls).delete()
    db.session.query(Responses).delete()
    db.session.commit()


class BasicTests(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(BasicTests, self).__init__(*args, **kwargs)
        self.email = 'test@test.com'
        self.password = 'mypassword'
        self.client = app.test_client()

        sha256_crypt.encrypt = MagicMock(side_effect=lambda password: password)
        sha256_crypt.verify = MagicMock(side_effect=lambda password, hash: password == hash)

    def setUp(self):
        db.create_all()

    def tearDown(self):
        self.logout()

    def register_login(self, email=None, password=None):
        if email is None:
            email = self.email
        if password is None:
            password = self.password

        return self.client.post(
            '/register',
            data=dict(email=email, password=password),
            follow_redirects=True
        )

    def register_only(self, email=None, password=None):
        if email is None:
            email = self.email
        if password is None:
            password = self.password

        with patch('app.helpers.login_user'):
            return self.client.post(
                '/register',
                data=dict(email=email, password=password),
                follow_redirects=True
            )

    def login(self, email=None, password=None):
        if email is None:
            email = self.email
        if password is None:
            password = self.password

        return self.client.post(
            '/login',
            data=dict(email=email, password=password),
            follow_redirects=True
        )

    def logout(self):
        return self.client.get(
            '/logout',
            follow_redirects=True
        )

    def create_poll(self, title, options):
        return self.client.post(
            '/create',
            data=dict(title=title, optionA=options[0],
                      optionB=options[1]),
            follow_redirects=True
        )

    def test_index_up(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_valid_registration(self):
        clear_users()
        response = self.register_only()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Users.query.filter_by(email=self.email).count(), 1)

    def test_invalid_registration(self):
        clear_users()
        response = self.register_only()
        self.logout()
        response = self.register_only()
        self.assertIn(b'That email has already been used to register',
                      response.data)

    def test_valid_login(self):
        self.register_only()
        response = self.login()
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Dashboard', response.data)

    def test_invalid_login_email(self):
        self.register_only()
        response = self.login('bademail@test.com', self.password)
        self.assertIn(b'Incorrect email or password', response.data)

    def test_invalid_login_password(self):
        self.register_only()
        response = self.login(self.email, 'badpassword')
        self.assertIn(b'Incorrect email or password', response.data)

    def test_valid_logout(self):
        self.register_login()
        response = self.logout()
        self.assertEqual(response.status_code, 200)

    def test_invalid_logout(self):
        response = self.logout()
        self.assertEqual(response.status_code, 200)

    def test_create_poll(self):
        clear_polls()
        self.register_login()
        response = self.create_poll('Test poll', ['Option A', 'Option B'])
        self.assertIn(b"Poll created", response.data)

    def test_view_poll(self):
        self.register_login()
        self.create_poll('Test poll', ['Option A', 'Option B'])
        response = self.client.get('/view')
        self.assertIn(b"Test poll", response.data)
        self.assertIn(b"Option A", response.data)
        self.assertIn(b"Option B", response.data)

    def test_login_validated(self):
        # Test that a valid login is required to
        # access the dashboard, or some other webpage
        pass

    def test_login_invalidated(self):
        pass


if __name__ == "__main__":
    unittest.main()
