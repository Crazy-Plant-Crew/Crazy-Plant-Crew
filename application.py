import os
import urllib.parse
import sys
import traceback
import requests
import base64
import json
import random
import string

from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename
from functools import wraps
from itsdangerous import URLSafeTimedSerializer
from flask_mail import Message, Mail
from time import time
from flask_ckeditor import CKEditor
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text


# Configure application
app = Flask(__name__)


# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True


# Set secret key for site
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY") 


# Configure DB
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# DB Schemas
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True, unique=True)
    username = db.Column(db.String(255), nullable=False, unique=True)
    email = db.Column(db.String(255), nullable=False, unique=True)
    hash = db.Column(db.String(255), nullable=False, unique=True)
    role = db.Column(db.String(255), nullable=False, default="user")
    picture = db.Column(db.String(255), nullable=False, default="/static/profile.svg")
    confirmed = db.Column(db.String(255), nullable=False, default="False")
    time = db.Column(db.Integer, nullable=False, default=0)
    pin = db.Column(db.Integer, nullable=False, default=0)
    newsletter = db.Column(db.String(255), nullable=False, default="True")

class Plants(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True, unique=True)
    name = db.Column(db.String(255), nullable=False, default="No name")
    stock = db.Column(db.Integer, nullable=False, default=0)
    price = db.Column(db.Integer, nullable=False, default=0)
    picture = db.Column(db.String(255), nullable=False, default="https://i.ibb.co/QNJnLR8/empty.png")
    description = db.Column(db.String(255), nullable=False, default="No description")
    show = db.Column(db.String(255), nullable=False, default="False")

class News(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True, unique=True)
    title = db.Column(db.String(255), nullable=False, default="No title")
    body = db.Column(db.String(255), nullable=False, default="No body")

class Baskets(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True, unique=True)
    user_id = db.Column(db.Integer, nullable=False)
    plant_id = db.Column(db.Integer, nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=0)
    name = db.Column(db.String(255), nullable=False, default="No name")
    picture = db.Column(db.String(255), nullable=False, default="https://i.ibb.co/QNJnLR8/empty.png")
    price = db.Column(db.Integer, nullable=False)
    subtotal = db.Column(db.Integer, nullable=False, default=0)


# Create DB
db.create_all()


# Seed DB for admin
result = db.engine.execute(text("SELECT * FROM Users WHERE username='\:username';", {"username": os.environ.get("USERNAME")}))
query = result.fetchall()

if len(query) == 0:
    db.engine.execute(text("INSERT INTO Users(username, email, hash, role, picture, confirmed, time, pin, newsletter) VALUES (\:username', '\:email', '\:hash', '\:role', '\:picture', '\:confirmed', '\:time', '\:pin', '\:newsletter')", {"username": os.environ.get("USERNAME"), "email": os.environ.get("EMAIL"), "hash": generate_password_hash(os.environ.get("PASSWORD")), "role": os.environ.get("ROLE"), "picture": "/static/profile.svg", "confirmed": os.environ.get("CONFIRMED"), "time": 0, "pin": 0, "newsletter": "True"}))
    
    """
    db.session.add(Users(username=os.environ.get("USERNAME"), email=os.environ.get("EMAIL"), hash=generate_password_hash(os.environ.get("PASSWORD")), role=os.environ.get("ROLE"), confirmed=os.environ.get("CONFIRMED")))
    db.session.commit()
    """



# Set CKEditor
ckeditor = CKEditor(app)


# Email configuration
app.config["DEBUG"] = False
app.config["BCRYPT_LOG_ROUNDS"] = 13
app.config["WTF_CSRF_ENABLED"] = True
app.config["DEBUG_TB_ENABLED"] = False
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False
app.config["MAIL_SERVER"] = "smtp.googlemail.com"
app.config["MAIL_PORT"] = 465
app.config["MAIL_USE_TLS"] = False
app.config["MAIL_USE_SSL"] = True
app.config["MAIL_USERNAME"] = os.environ["APP_MAIL_USERNAME"]
app.config["MAIL_PASSWORD"] = os.environ["APP_MAIL_PASSWORD"]
app.config["MAIL_DEFAULT_SENDER"] = "crazy.plant.crew.2020@gmail.com"


# Configure mail 
mail = Mail(app)


# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


# Define allowed extensions
ALLOWED_EXTENSIONS = {'jpg', 'png', 'bmp', 'gif', 'tif', 'webp', 'heic', 'pdf'}


# Handle errors
def errorhandler(e):

    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()

    return flash(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)


# Decorator to ensure user must be logged in
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):

        if session.get("user_id") is None:
            return redirect("/signin")

        return f(*args, **kwargs)

    return decorated_function


# Decorator to ensure user is confirmed via email
def confirmed_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):

        if getUserConfirmed() == "False":

            flash("Please enter the PIN code sent to the given email address")
            return redirect("/unconfirmed")

        return f(*args, **kwargs)

    return decorated_function


# Decorator to ensure user is authorized
def role_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):

        if getUserRole() == "user":

            flash("You are not authorized to access this page")
            return redirect("/")

        return f(*args, **kwargs)

    return decorated_function


# Check if captcha is valided
def is_human(captcha_response):

    secret = os.environ.get("SITE_SECRET_KEY")
    payload = {'response':captcha_response, 'secret':secret}
    response = requests.post("https://www.google.com/recaptcha/api/siteverify", payload)
    response_text = json.loads(response.text)

    return response_text['success']


# Generate random password
def randomPassword():
    
    result = ""
    while len(result) <= 12:
        character = random.choice(string.printable)
        result += character
    
    return result


# Define allowed file extensions for upload
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# ImgBB API upload function
def uploadPicture(upload):

    # Contact API
    try:
                    
        with open(upload, "rb") as file:

            url = "https://api.imgbb.com/1/upload"
            payload = {
                "key": os.environ.get("IMGBB_API"),
                "image": base64.b64encode(file.read())
            }

            response = requests.post(url, payload)

    except requests.RequestException:

        return None

    # Parse response
    try:

        image = response.json()
        dbReturn =  {
            "picture": image["data"]["url"],
        }
        return dbReturn["picture"]

    except (KeyError, TypeError, ValueError):

        return None


# Send PIN code with confirmation email and save it to database
def sendPin(email):

    # Create activation email with a random PIN
    pin = random.randint(100000,999999)
    subject = "Welcome!"
    body = render_template('activate.html', name=getUserName(), pin=pin)
    user_id = session["user_id"]
    date = int(time())

    messsage = Message(subject=subject, recipients=[email], body=body)
    mail.send(messsage)    

    db.engine.execute("UPDATE Users SET time=:date, pin=:pin WHERE id=:id;", {"date": date, "pin": pin, "id": user_id})


# Send email
def sendMail(subject, email, body):
    messsage = Message(subject=subject, recipients=[email], body=body)
    mail.send(messsage)


# Check if user is confirmed via email
def getUserConfirmed():

    # Check who's id is logged in
    loggedId = session["user_id"]
        
    # Query database for unconfirmed user
    record = db.engine.execute("SELECT confirmed FROM Users WHERE id=:id;", {"id": loggedId})
    confirmed = record.fetchall()[0][0]

    return confirmed


# Get username to be displayed 
def getUserName():

    # Check who's id is logged in
    loggedId = session["user_id"]
    
    # Query database for username
    record = db.engine.execute("SELECT username FROM Users WHERE id=:id;", {"id": loggedId})
    name = record.fetchall()[0][0]

    return name


# Get the user email address
def getUserEmail():

    # Check who's id is logged in
    loggedId = session["user_id"]
    
    # Query database for email
    record = db.engine.execute("SELECT email FROM Users WHERE id=:id;", {"id": loggedId})
    email = record.fetchall()[0][0]
        
    return email


# Get the user role
def getUserRole():

    loggedId = session["user_id"]
    
    # Query database for role
    record = db.engine.execute("SELECT role FROM Users WHERE id=:id;", {"id": loggedId})
    role = record.fetchall()[0][0]
        
    return role


# Get the user current PIN
def getUserPin():

    # Check who's id is logged in
    loggedId = session["user_id"]
    
    # Query database for PIN
    record = db.engine.execute("SELECT pin FROM Users WHERE id=:id", {"id": loggedId})
    pin = record.fetchall()[0][0]
        
    return pin


# Get the user registration time
def getUserTime():

    # Check who's id is logged in
    loggedId = session["user_id"]
    
    # Query database for time
    record = db.engine.execute("SELECT time FROM Users WHERE id=:id;", {"id": loggedId})
    time = record.fetchall()[0][0]
        
    return time


# Get profile picture to be displayed 
def getUserPicture():

    # Check who's id is logged in
    loggedId = session["user_id"]
    
    # Query database for picture
    record = db.engine.execute("SELECT picture FROM Users WHERE id=:id;", {"id": loggedId})
    picture = record.fetchall()[0][0]
        
    return picture


# Import routes after to avoid circular import
from routes.profile import profile
from routes.message import message
from routes.index import index
from routes.signup import signup
from routes.logout import logout
from routes.signin import signin
from routes.username import username
from routes.password import password
from routes.mailing import mailing
from routes.email import email
from routes.picture import picture
from routes.delete import delete
from routes.article import article
from routes.unconfirmed import unconfirmed
from routes.forget import forget
from routes.administration import administration
from routes.add import add
from routes.edit import edit
from routes.remove import remove
from routes.communication import communication
from routes.newsletter import newsletter
from routes.basket import basket
from routes.about import about
from routes.change import change
from routes.create import create
from routes.pay import pay
from routes.transaction import transaction
from routes.history import history


# Configure Blueprints
app.register_blueprint(signin)
app.register_blueprint(signup)
app.register_blueprint(logout)
app.register_blueprint(index)
app.register_blueprint(profile)
app.register_blueprint(message)
app.register_blueprint(username)
app.register_blueprint(password)
app.register_blueprint(mailing)
app.register_blueprint(email)
app.register_blueprint(picture)
app.register_blueprint(delete)
app.register_blueprint(article)
app.register_blueprint(unconfirmed)
app.register_blueprint(forget)
app.register_blueprint(administration)
app.register_blueprint(add)
app.register_blueprint(edit)
app.register_blueprint(remove)
app.register_blueprint(newsletter)
app.register_blueprint(communication)
app.register_blueprint(basket)
app.register_blueprint(about)
app.register_blueprint(change)
app.register_blueprint(create)
app.register_blueprint(pay)
app.register_blueprint(transaction)
app.register_blueprint(history)