import os
import sqlite3
import urllib.parse
import sys
import traceback
import requests
import base64
import json

from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename
from functools import wraps
from itsdangerous import URLSafeTimedSerializer

# Configure application
app = Flask(__name__)


# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True


# Set secre"t key for site
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY") 


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


# Handle eorrs
def errorhandler(e):

    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()

    return flash(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)


# Ensure user must be logged in
def login_required(f):
    """
    Decorate routes to require login.
    http://flask.pocoo.org/docs/1.0/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):

        if session.get("user_id") is None:
            return redirect("/signin")

        return f(*args, **kwargs)

    return decorated_function


def is_human(captcha_response):
    """ Validating recaptcha response from google server
        Returns True captcha test passed for submitted form else returns False.
    """
    secret = os.environ.get("SITE_SECRET_KEY")
    payload = {'response':captcha_response, 'secret':secret}
    response = requests.post("https://www.google.com/recaptcha/api/siteverify", payload)
    response_text = json.loads(response.text)
    return response_text['success']


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


# Get username to be displayed 
def profileName():

    try:

        sqliteConnection = sqlite3.connect("database.db")
        cursor = sqliteConnection.cursor()

        # Check who's id is logged in
        loggedId = session["user_id"]
        
        # Query database for username
        cursor.execute("SELECT username FROM users WHERE id=:id", {"id": loggedId})
        name = cursor.fetchall()[0][0]

        cursor.close()

    except sqlite3.Error as error:
    
        print("Failed to read data from sqlite table", error)
        print("Exception class is: ", error.__class__)
        print("Exception is", error.args)

        print('Printing detailed SQLite exception traceback: ')
        exc_type, exc_value, exc_tb = sys.exc_info()
        print(traceback.format_exception(exc_type, exc_value, exc_tb))

    finally:
    
        if (sqliteConnection):
            sqliteConnection.close()   
        
        return name


# Get profile picture to be displayed 
def profilePicture():

    try:

        sqliteConnection = sqlite3.connect("database.db")
        cursor = sqliteConnection.cursor()

        # Check who's id is logged in
        loggedId = session["user_id"]
        
        # Query database for username
        cursor.execute("SELECT picture FROM users WHERE id=:id", {"id": loggedId})
        picture = cursor.fetchall()[0][0]

        cursor.close()

    except sqlite3.Error as error:
    
        print("Failed to read data from sqlite table", error)
        print("Exception class is: ", error.__class__)
        print("Exception is", error.args)

        print('Printing detailed SQLite exception traceback: ')
        exc_type, exc_value, exc_tb = sys.exc_info()
        print(traceback.format_exception(exc_type, exc_value, exc_tb))

    finally:
    
        if (sqliteConnection):
            sqliteConnection.close()   
        
        return picture

"""
# Confirmation token generator
def generate_confirmation_token(email):

    serializer = URLSafeTimedSerializer(app.config["SITE_SECRET_KEY"])

    return serializer.dumps(email, salt=app.config["SECURITY_PASSWORD_SALT"])


# Confirmation token checker
def confirm_token(token, expiration=3600):

    serializer = URLSafeTimedSerializer(app.config["SITE_SECRET_KEY"])

    try:
        email = serializer.loads(token, salt=app.config["SECURITY_PASSWORD_SALT"], max_age=expiration)

    except:

        return False

    return email


# Email configuration
# main config
SECRET_KEY = "CPC2020SK!!"
SECURITY_PASSWORD_SALT = "CPC2020SPS!!"
DEBUG = False
BCRYPT_LOG_ROUNDS = 13
WTF_CSRF_ENABLED = True
DEBUG_TB_ENABLED = False
DEBUG_TB_INTERCEPT_REDIRECTS = False

# mail settings
MAIL_SERVER = 'smtp.googlemail.com'
MAIL_PORT = 465
MAIL_USE_TLS = False
MAIL_USE_SSL = True

# gmail authentication
MAIL_USERNAME = os.environ['APP_MAIL_USERNAME']
MAIL_PASSWORD = os.environ['APP_MAIL_PASSWORD']

# mail accounts
MAIL_DEFAULT_SENDER = "crazy.plant.crew.2020@gmail.com"
"""


# Import routes after to avoid circular import
from routes.profile import profile
from routes.message import message
from routes.index import index
from routes.signup import signup
from routes.logout import logout
from routes.signin import signin
from routes.username import username
from routes.password import password
from routes.email import email
from routes.picture import picture
from routes.delete import delete


# Configure Blueprints
app.register_blueprint(signin)
app.register_blueprint(signup)
app.register_blueprint(logout)
app.register_blueprint(index)
app.register_blueprint(profile)
app.register_blueprint(message)
app.register_blueprint(username)
app.register_blueprint(password)
app.register_blueprint(email)
app.register_blueprint(picture)
app.register_blueprint(delete)
