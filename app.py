from flask import flash, Flask, redirect, render_template, request, session
from flask_sqlalchemy import SQLAlchemy
from passlib.hash import sha256_crypt
import os

DB_URL = os.environ["DATABASE_URL"]

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
app.secret_key = 'D\xaec\xb7\x85\x01\x0e\x8c\x05\x94\xd1\xc83\x92Z\xd7\xfe\x04\x11\xe3[\x91\xf7\xe4'

db = SQLAlchemy(app)

# Create table schemes
class Users(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.Text, nullable = False)
    password = db.Column(db.Text, nullable = False)

@app.route('/index')
@app.route('/')
def index():
    return render_template('index.html', user = 'user' in session)
    
@app.route('/register', methods = ['POST', 'GET'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        hash_password = sha256_crypt.encrypt(password)
        
        if Users.query.filter_by(email = email).first():
            flash("That email has already been used to register. You can <a href = '/login'>login here</a>")
            return render_template('register.html')
        
        new_user = Users(email = email, password = hash_password)
        db.session.add(new_user)
        db.session.commit()
        
        session['user'] = email
        
        return redirect('/dashboard')

@app.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        hash_password = sha256_crypt.encrypt(password)
        
        user = Users.query.filter_by(email = email).first()
        
        if not user:
            flash("Incorrect email")
            return render_template('login.html')
        
        if not sha256_crypt.verify(password, user.password):
            flash("Incorrect password")
            return render_template('login.html')
        
        session['user'] = email
        
        return redirect('/dashboard')
        

@app.route('/dashboard')
def dashboard():
    # TODO: verify that user is logged in to view this page
    return render_template('dashboard.html', user = session['user'])

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(debug = True, host = '0.0.0.0', port = port)
