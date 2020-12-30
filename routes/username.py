import sqlite3
import traceback
import sys
import re

from flask import Blueprint, render_template, redirect, session, request, flash, get_flashed_messages
from application import profileName, profilePicture, login_required, check_confirmed

# Set Blueprints
username = Blueprint('username', __name__,)

@username.route("/username", methods=["GET", "POST"])
@login_required
@check_confirmed
def usernameFunction():

    # Force flash() to get the messages on the same page as the redirect.
    get_flashed_messages()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        username = request.form.get("username")

        # Ensure username was submitted
        if not username:
            flash("must provide username")
            return redirect("/username")

        # Ensure username fits server-side
        if not re.search("^[a-zA-Z0-9]{2,20}$", username):
            flash("Invalid username")
            return redirect("/username")


        # Query database for username if already exists
        try:

            sqliteConnection = sqlite3.connect("database.db")
            cursor = sqliteConnection.cursor()
            
            # Query database for username
            cursor.execute("SELECT * FROM users WHERE username=:username;", {"username": username})
            record = cursor.fetchall()

            # Check if username is free
            if len(record) != 1:
                flash("Username already taken")
                return redirect("/username")

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


        # Update database with username
        try:

            sqliteConnection = sqlite3.connect("database.db")
            cursor = sqliteConnection.cursor()
            user_id = session["user_id"]
            
            # Update database for username
            cursor.execute("UPDATE users SET username=:username WHERE id=:user_id;", {"username": username, "user_id": user_id})
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

        return redirect("/profile")
    
    else:

        return render_template("username.html", name=profileName(), picture=profilePicture())