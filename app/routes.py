"""File that stores all of the pollz app's routes, or adresses that can be
visited, as defined by the app.route decorators."""

from flask import redirect, flash, request, session
from passlib.hash import sha256_crypt
from app import app, db
from app.helpers import login_user, render_with_user, add_poll, json_response
from app.models import Users, Polls, Options


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

        if Users.query.filter(Users.email == email).count():
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

        user = Users.query.filter(Users.email == email).first()

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

    polls = [{'title': poll.title, 'id': poll.id, 'options': enumerate(poll.options)}
             for poll in Polls.query.join(Options).order_by(Polls.id).all()]

    return render_with_user('view.html', polls=polls)


@app.route('/create', methods=['GET', 'POST'])
def create():
    """Path that serves a form to create a new form is the user is logged in,
    and handles the response when the form is submitted"""

    if 'user' not in session:
        flash('You must login before you can create a poll')
        return redirect('/login')

    elif request.method == 'POST':
        title = request.form.get('title')
        options = request.form.getlist('options[]')

        add_poll(title, options)
        db.session.commit()

        flash('Poll created')
        return redirect('/dashboard')

    return render_with_user('create.html')


@app.route('/vote')
def vote():
    """Route that is used to submit votes to the database.
    GET is used to submit requests, to add a vote
    to the database, switch a vote, or remove a vote, as
    determined by client-side javascript."""

    poll_id = request.args.get('poll_id')
    option = request.args.get('option', type=int)
    previous_option = request.args.get('previous_option', type=int)
    method = request.args.get('method')

    if poll_id is None or option is None:
        return redirect('/view')

    poll = Polls.query.join(Options).filter(Polls.id == poll_id).first()

    if method == 'add':
        poll.options[option].votes = poll.options[option].votes + 1

    elif method == 'change':
        poll.options[option].votes = poll.options[option].votes + 1
        poll.options[previous_option].votes = poll.options[previous_option].votes - 1

    elif method == 'remove':
        poll.options[option].votes = poll.options[option].votes - 1

    else:
        return (400, 'Bad Request')

    db.session.commit()

    data = [{'text': poll_option.text, 'votes': poll_option.votes} for poll_option in poll.options]

    return json_response(data)
