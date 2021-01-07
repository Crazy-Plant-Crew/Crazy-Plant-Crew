import os
import sqlite3
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

# Configure application
app = Flask(__name__)


# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True


# Set secret key for site
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY") 


# Set CKEditor
ckeditor = CKEditor(app)


# Email configuration
app.config["SECURITY_PASSWORD_SALT"] = os.environ["EMAIL_SECURITY_PASSWORD_SALT"]
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


# Handle eorrs
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

    try:

        sqliteConnection = sqlite3.connect("database.db")
        cursor = sqliteConnection.cursor()
        
        cursor.execute("UPDATE users SET time=:date, pin=:pin WHERE id=:id;", {"date": date, "pin": pin, "id": user_id})
        sqliteConnection.commit()

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


# Send email
def sendMail(subject, email, body):
    messsage = Message(subject=subject, recipients=[email], body=body)
    mail.send(messsage)


# Check if user is confirmed via email
def getUserConfirmed():
    try:

        sqliteConnection = sqlite3.connect("database.db")
        cursor = sqliteConnection.cursor()

        # Check who's id is logged in
        loggedId = session["user_id"]
        
        # Query database for unconfirmed user
        cursor.execute("SELECT confirmed FROM users WHERE id=:id;", {"id": loggedId})
        confirmed = cursor.fetchall()[0][0]

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

    return confirmed


# Get username to be displayed 
def getUserName():

    try:

        sqliteConnection = sqlite3.connect("database.db")
        cursor = sqliteConnection.cursor()

        # Check who's id is logged in
        loggedId = session["user_id"]
        
        # Query database for username
        cursor.execute("SELECT username FROM users WHERE id=:id;", {"id": loggedId})
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


# Get the user email address
def getUserEmail():

    try:

        sqliteConnection = sqlite3.connect("database.db")
        cursor = sqliteConnection.cursor()

        # Check who's id is logged in
        loggedId = session["user_id"]
        
        # Query database for email
        cursor.execute("SELECT email FROM users WHERE id=:id;", {"id": loggedId})
        email = cursor.fetchall()[0][0]

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
        
        return email


# Get the user role
def getUserRole():

    try:

        sqliteConnection = sqlite3.connect("database.db")
        cursor = sqliteConnection.cursor()

        # Check who's id is logged in
        loggedId = session["user_id"]
        
        # Query database for role
        cursor.execute("SELECT role FROM users WHERE id=:id;", {"id": loggedId})
        role = cursor.fetchall()[0][0]

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
        
        return role


# Get the user current PIN
def getUserPin():

    try:

        sqliteConnection = sqlite3.connect("database.db")
        cursor = sqliteConnection.cursor()

        # Check who's id is logged in
        loggedId = session["user_id"]
        
        # Query database for PIN
        cursor.execute("SELECT pin FROM users WHERE id=:id", {"id": loggedId})
        pin = cursor.fetchall()[0][0]

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
        
        return pin


# Get the user registration time
def getUserTime():

    try:

        sqliteConnection = sqlite3.connect("database.db")
        cursor = sqliteConnection.cursor()

        # Check who's id is logged in
        loggedId = session["user_id"]
        
        # Query database for time
        cursor.execute("SELECT time FROM users WHERE id=:id;", {"id": loggedId})
        time = cursor.fetchall()[0][0]

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
        
        return time


# Get profile picture to be displayed 
def getUserPicture():

    try:

        sqliteConnection = sqlite3.connect("database.db")
        cursor = sqliteConnection.cursor()

        # Check who's id is logged in
        loggedId = session["user_id"]
        
        # Query database for picture
        cursor.execute("SELECT picture FROM users WHERE id=:id;", {"id": loggedId})
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