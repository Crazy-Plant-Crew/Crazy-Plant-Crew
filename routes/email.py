import sqlite3
import traceback
import sys
import re

from flask import Blueprint, render_template, redirect, session, request, flash, get_flashed_messages
from application import getUserName, getUserPicture, login_required, confirmed_required, getUserRole

# Set Blueprints
email = Blueprint('email', __name__,)

@email.route("/email", methods=["GET", "POST"])
@login_required
@confirmed_required
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
        if not re.search(r"[^@]+@[^@]+\.[^@]+", email):
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

        flash("Email address updated")
        return redirect("/profile")

    return render_template("email.html", name=getUserName(), picture=getUserPicture(), role=getUserRole())