import sqlite3
import traceback
import sys

from flask import Blueprint, render_template, redirect, session, request, flash
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

# Set Blueprints
signup = Blueprint('signup', __name__,)

@signup.route("/signup", methods=["GET", "POST"])
def signupFunction():

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        email = request.form.get("email")
        username = request.form.get("username")
        password = request.form.get("password")
        confirmPassword  = request.form.get("confirm-password")

        # Ensure email was submitted
        if not email:
            return flash("must provide email")
        # Ensure username was submitted
        if not username:
            return flash("must provide username")

        # Ensure password was submitted
        if not password:
            return flash("must provide password")

        # Ensure confirm password is correct
        if password != confirmPassword:
            return flash("The passwords don't match")

        # Query database for username if already exists
        try:

            sqliteConnection = sqlite3.connect("database.db")
            cursor = sqliteConnection.cursor()
            
            # Query database for username
            cursor.execute("SELECT * FROM users WHERE username=:username;", {"username": username})
            record = cursor.fetchall()

            # Check if username is free
            if record == username: 
                return flash("Username already taken")

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
        

        # Insert user and hash of the password into the table
        try:

            sqliteConnection = sqlite3.connect("database.db")
            cursor = sqliteConnection.cursor()
            
            cursor.execute("INSERT INTO users(username, hash, email) VALUES (:username, :hash, :email);", {"username": username, "hash": generate_password_hash(password), "email": email})
            record = sqliteConnection.commit()

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
            

        # Query database for username & remember which user has logged in
        try:

            sqliteConnection = sqlite3.connect("database.db")
            cursor = sqliteConnection.cursor()
            
            # Query database for username
            cursor.execute("SELECT * FROM users WHERE username=:username;", {"username": username})
            record = cursor.fetchall()
            
            # Remember which user has logged in
            session["user_id"] = record[0][0]

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

        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("signup.html")

