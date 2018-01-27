# TODO: prepopulate db with some users and polls, clear
# polls/users must add them back, or do something else

import unittest
from mock import MagicMock, patch
from context import app, db, Users, Polls, Responses, sha256_crypt  # pylint:disable=W0403


TEST_DB = 'sqlite:///:memory:'


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
        self.app = app.test_client()

        sha256_crypt.encrypt = MagicMock(side_effect=lambda password: password)
        sha256_crypt.verify = MagicMock(side_effect=lambda password, hash: password == hash)
        app.config['SQLALCHEMY_DATABASE_URI'] = TEST_DB
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    def setUp(self):
        db.create_all()

    def tearDown(self):
        self.logout()

    def register_login(self, email=None, password=None):
        if email is None:
            email = self.email
        if password is None:
            password = self.password

        return self.app.post(
            '/register',
            data=dict(email=email, password=password),
            follow_redirects=True
        )

    def register_only(self, email=None, password=None):
        if email is None:
            email = self.email
        if password is None:
            password = self.password

        with patch('app.login_user'):
            return self.app.post(
                '/register',
                data=dict(email=email, password=password),
                follow_redirects=True
            )

    def login(self, email=None, password=None):
        if email is None:
            email = self.email
        if password is None:
            password = self.password

        return self.app.post(
            '/login',
            data=dict(email=email, password=password),
            follow_redirects=True
        )

    def logout(self):
        return self.app.get(
            '/logout',
            follow_redirects=True
        )

    def create_poll(self, title, options):
        return self.app.post(
            '/create',
            data=dict(title=title, optionA=options[0],
                      optionB=options[1]),
            follow_redirects=True
        )

    def test_index_up(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)

    def test_valid_registration(self):
        clear_users()
        response = self.register_only()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Users.query.filter_by(email=self.email).count(), 1)

    def test_invalid_registration(self):
        clear_users()
        response = self.register_only()
        response = self.register_only()
        self.assertIn('That email has already been used to register',
                      response.data)

    def test_valid_login(self):
        self.register_only()
        response = self.login()
        self.assertEqual(response.status_code, 200)
        self.assertIn('Dashboard', response.data)

    def test_invalid_login_email(self):
        self.register_only()
        response = self.login('bademail@test.com', self.password)
        self.assertIn('Incorrect email or password', response.data)

    def test_invalid_login_password(self):
        self.register_only()
        response = self.login(self.email, 'badpassword')
        self.assertIn('Incorrect email or password', response.data)

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
        self.assertIn("Poll created", response.data)

    def test_view_poll(self):
        self.register_login()
        self.create_poll('Test poll', ['Option A', 'Option B'])
        response = self.app.get('/view')
        self.assertIn("Test poll", response.data)
        self.assertIn("Option A", response.data)
        self.assertIn("Option B", response.data)

    def test_login_validated(self):
        # Test that a valid login is required to
        # access the dashboard, or some other webpage
        pass

    def test_login_invalidated(self):
        pass


if __name__ == "__main__":
    unittest.main()
