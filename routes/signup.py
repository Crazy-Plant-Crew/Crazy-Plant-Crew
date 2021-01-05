import sqlite3
import traceback
import sys
import os
import re

from flask import Blueprint, render_template, redirect, session, request, flash, get_flashed_messages
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename
from application import uploadPicture, is_human, sendPin
from time import time


# Set Blueprints
signup = Blueprint('signup', __name__,)

# Assign public key
pub_key = os.environ.get("SITE_KEY")

@signup.route("/signup", methods=["GET", "POST"])
def signupFunction():

    # Force flash() to get the messages on the same page as the redirect.
    get_flashed_messages()

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        email = request.form.get("email")
        username = request.form.get("username")
        password = request.form.get("password")
        confirmPassword  = request.form.get("confirm-password")
        captcha_response = request.form['g-recaptcha-response']

        # token = generate_confirmation_token(email)

        # Ensure captcha was correct
        if is_human(captcha_response) != True:
            flash("must completed captcha")
            return redirect("/signup")

            
        # Ensure email was submitted
        if not email:
            flash("must provide email")
            return redirect("/signup")

        # Ensure username was submitted
        if not username:
            flash("must provide username")
            return redirect("/signup")

        # Ensure password was submitted
        if not password:
            flash("must provide password")
            return redirect("/signup")

        # Ensure confirm password is correct
        if password != confirmPassword:
            flash("The passwords don't match")
            return redirect("/signup")

        # Ensure username fits server-side
        if not re.search("^[a-zA-Z0-9]{2,20}$", username):
            flash("Invalid username")
            return redirect("/signup")

        # Ensure email fits server-side
        if not re.search(r"^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$", email):
            flash("Invalid email")
            return redirect("/signup")


        # Query database for username if already exists
        try:

            sqliteConnection = sqlite3.connect("database.db")
            cursor = sqliteConnection.cursor()
            
            # Query database for username
            cursor.execute("SELECT * FROM users WHERE username=:username;", {"username": username})
            record = cursor.fetchall()

            # Check if username is free
            if len(record) != 0:
                flash("Username already taken")
                return redirect("/signup")

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


        # Query database for email if already exists
        try:

            sqliteConnection = sqlite3.connect("database.db")
            cursor = sqliteConnection.cursor()
            
            # Query database for email
            cursor.execute("SELECT * FROM users WHERE email=:email;", {"email": email})
            record = cursor.fetchall()

            # Check if email is free
            if len(record) != 0:
                flash("Email already taken")
                return redirect("/signup")
            
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
        

        # Insert username, email and hash of the password into the table
        try:

            sqliteConnection = sqlite3.connect("database.db")
            cursor = sqliteConnection.cursor()
            
            cursor.execute("INSERT INTO users(username, hash, email) VALUES (:username, :hash, :email)", {"username": username, "hash": generate_password_hash(password), "email": email})
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

        
        # Save, upload and delete picture file
        file = request.files["picture"]

        if file and file.filename:

            filename = secure_filename(file.filename)
            file.save(os.path.join("./static", filename))
            upload = uploadPicture("./static/" + filename)
            os.remove("./static/" + filename)

            # Update database with new image url 
            try:

                sqliteConnection = sqlite3.connect("database.db")
                cursor = sqliteConnection.cursor()
                user_id = session["user_id"]
                
                cursor.execute("UPDATE users SET picture=:picture WHERE id=:id;", {"picture": upload, "id": user_id})
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

        
        sendPin(email)

        return redirect("/")

    
    # User reached route via GET (as by clicking a link or via redirect)
    else:

        return render_template("signup.html", pub_key=pub_key)

