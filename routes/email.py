import sqlite3
import traceback
import sys
import re

from flask import Blueprint, render_template, redirect, session, request, flash, get_flashed_messages
from application import profileName, profilePicture, login_required, check_confirmed

# Set Blueprints
email = Blueprint('email', __name__,)

@email.route("/email", methods=["GET", "POST"])
@login_required
@check_confirmed
def emailFunction():

    # Force flash() to get the messages on the same page as the redirect.
    get_flashed_messages()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        email = request.form.get("email")

        # Ensure email was submitted
        if not email:
            flash("must provide email")
            return redirect("/email")

        # Ensure email fits server-side
        if not re.search(r"^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$", email):
            flash("Invalid email")
            return redirect("/email")


        # Query database for email if already exists
        try:

            sqliteConnection = sqlite3.connect("database.db")
            cursor = sqliteConnection.cursor()
            
            # Query database for email
            cursor.execute("SELECT * FROM users WHERE email=:email;", {"email": email})
            record = cursor.fetchall()

            # Check if email is free
            if len(record) != 1:
                flash("Email already taken")
                return redirect("/email")

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


        # Update database with email
        try:

            sqliteConnection = sqlite3.connect("database.db")
            cursor = sqliteConnection.cursor()
            user_id = session["user_id"]
            
            # Update database with email
            cursor.execute("UPDATE users SET email=:email WHERE id=:user_id;", {"email": email, "user_id": user_id})
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

    return render_template("email.html", name=profileName(), picture=profilePicture())