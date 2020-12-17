import os
import sqlite3
import urllib.parse
import sys
import traceback
import requests

from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from functools import wraps

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

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

# ImgBB API upload function
def uploadPicture(file):

    # Contact API
    try:
        api_key = os.environ.get("IMGBB_API")
        response = requests.post(f"https://api.imgbb.com/1/upload?expiration=600&key={api_key}")
        response.raise_for_status()
    except requests.RequestException:
        return None

    # Parse response
    try:
        image = response.json()
        file = {
            "picture": image["data"]["url"],
        }
        return file
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
