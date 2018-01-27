# TODO: add custom functions for rendering
# templates with info on user logged in, title, etc

# TODO: add function that verifies user is logged in
# or not, redirects appropriaetly

import os
from flask import flash, Flask, redirect, render_template, request, session
from flask_sqlalchemy import SQLAlchemy
from passlib.hash import sha256_crypt

DB_URL = os.environ["DATABASE_URL"]

app = Flask(__name__)  # pylint: disable=C0103

app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'D\xaec\xb7\x85\x01\x0e\x8c\x05\x94\xd1\
                  \xc83\x92Z\xd7\xfe\x04\x11\xe3[\x91\xf7\xe4'

db = SQLAlchemy(app)  # pylint: disable=C0103


def login_user(email):
    session['user'] = email


class Users(db.Model):  # pylint: disable-msg=R0903
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.Text, nullable=False)
    password = db.Column(db.Text, nullable=False)


class Polls(db.Model):  # pylint: disable-msg=R0903
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text, nullable=False)
    responses = db.relationship('Responses')
    # TODO: add other settings
    #   Private/Public
    #   Timeout, cancelling, etc


class Responses(db.Model):  # pylint: disable-msg=R0903
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    poll_id = db.Column(db.Integer, db.ForeignKey(Polls.id), nullable=False)


@app.route('/index')
@app.route('/')
def index():
    return render_template('index.html', user=session.get('user'))


@app.route('/register', methods=['POST', 'GET'])
def register():
    # TODO: make sure user is not logged in
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        if Users.query.filter_by(email=email).count():
            flash("That email has already been used to register. \
                  You can <a href = '/login'>login here</a>")
            return render_template('register.html')

        hash_password = sha256_crypt.encrypt(password)
        new_user = Users(email=email, password=hash_password)
        db.session.add(new_user)
        db.session.commit()

        login_user(email)

        return redirect('/dashboard')

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    # TODO: make sure user is not logged in
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = Users.query.filter_by(email=email).first()

        if not user or not sha256_crypt.verify(password, user.password):
            flash("Incorrect email or password")
            return render_template('login.html')

        login_user(email)

        return redirect('/dashboard')

    return render_template('login.html')


@app.route('/logout')
def logout():
    if 'user' in session:
        session.pop('user')

    return redirect('/')


@app.route('/dashboard')
def dashboard():
    # TODO: verify that user is logged in to view this page
    # TODO: add function that verifies user is logged in, otherwise redirects
    return render_template('dashboard.html', user=session.get('user'))


@app.route('/view')
def view():
    polls = [[poll.title, poll.responses[0].text, poll.responses[1].text]
             for poll in Polls.query.join(Responses).all()]
    return render_template('view.html', polls=polls)


@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
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

    return render_template('create.html')


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(debug = True, host = '0.0.0.0', port = port)
