"""This file runs the Flask server for the Pollz Application."""

import os
from flask import flash, Flask, redirect, render_template, request, session
from flask_sqlalchemy import SQLAlchemy
from passlib.hash import sha256_crypt

DB_URL = os.environ.get("DATABASE_URL", 'sqlite:///dev.db')

app = Flask(__name__)  # pylint: disable=C0103

app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'D\xaec\xb7\x85\x01\x0e\x8c\x05\x94\xd1\
                  \xc83\x92Z\xd7\xfe\x04\x11\xe3[\x91\xf7\xe4'

db = SQLAlchemy(app)  # pylint: disable=C0103


def login_user(email):
    """Adds a user's email to their session to track that
    they have logged into the application."""

    session['user'] = email


def render_with_user(template, **kwargs):
    """Wrapper for flask's render_template function, that
    also passes the user's email (if they logged in) to the
    templating function."""

    return render_template(template, user=session.get('user'), **kwargs)


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


@app.route('/index')
@app.route('/')
def index():
    """Index page that is always served"""

    return render_with_user('index.html')


@app.route('/register', methods=['POST', 'GET'])
def register():
    """Path that serves a form to register, and processes
    the form upon submission. Users can't register while logged in"""

    if 'user' in session:
        return redirect('/dashboard')

    elif request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        if Users.query.filter_by(email=email).count():
            flash("That email has already been used to register. \
                  You can <a href = '/login'>login here</a>")
            return render_with_user('register.html')

        hash_password = sha256_crypt.encrypt(password)
        new_user = Users(email=email, password=hash_password)
        db.session.add(new_user)
        db.session.commit()

        login_user(email)

        return redirect('/dashboard')

    return render_with_user('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Path that serves a form to login, and processes
    the form upon submission. Users can't login twice"""

    if 'user' in session:
        return redirect('/dashboard')

    elif request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = Users.query.filter_by(email=email).first()

        if not user or not sha256_crypt.verify(password, user.password):
            flash("Incorrect email or password")
            return render_with_user('login.html')

        login_user(email)

        return redirect('/dashboard')

    return render_with_user('login.html')


@app.route('/logout')
def logout():
    """Path that will remove the user's email from the session,
    if they are logged in, and always redirect the user to the index page"""

    if 'user' in session:
        session.pop('user')

    return redirect('/')


@app.route('/dashboard')
def dashboard():
    """Dashboard path that can only be accessed when a user is logged in.
    Currently only displays the users email for testing purposes, but future
    implimentations may dispaly their polls, or their friends polls"""

    if 'user' not in session:
        return redirect('/login')

    return render_with_user('dashboard.html')


@app.route('/view')
def view():
    """View path that allows for rudimentary viewing of polls. Future implementations
    will allow users to brwose polls and vote on them."""

    polls = [[poll.title, poll.responses[0].text, poll.responses[1].text]
             for poll in Polls.query.join(Responses).all()]
    return render_with_user('view.html', polls=polls)


@app.route('/create', methods=['GET', 'POST'])
def create():
    """Path that serves a form to create a new form is the user is logged in,
    and handles the response when the form is submitted"""

    if 'user' not in session:
        return redirect('/login')

    elif request.method == 'POST':
        title = request.form.get('title')
        option_a = request.form.get('optionA')
        option_b = request.form.get('optionB')

        new_poll = Polls(title=title)
        db.session.add(new_poll)
        db.session.flush()

        option_a_row = Responses(text=option_a, poll_id=new_poll.id)
        option_b_row = Responses(text=option_b, poll_id=new_poll.id)

        db.session.add_all([option_a_row, option_b_row])
        db.session.commit()

        flash('Poll created')
        return redirect('/dashboard')

    return render_with_user('create.html')


if __name__ == '__main__':
    PORT = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host='0.0.0.0', port=PORT)
