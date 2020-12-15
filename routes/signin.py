import sqlite3
import traceback
import sys

from flask import Blueprint, render_template, redirect, session, request, flash
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

# Set Blueprints
signin = Blueprint('signin', __name__,)

@signin.route("/signin", methods=["GET", "POST"])
def signinFunction():

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")

        # Ensure username was submitted
        if not username:
            return flash("must provide username")

        # Ensure password was submitted
        if not password:
            return flash("must provide password")

        # Query database for username if already exists
        try:

            sqliteConnection = sqlite3.connect("database.db")
            cursor = sqliteConnection.cursor()
            
            # Query database for username
            cursor.execute("SELECT * FROM users WHERE username=:username", {"username": username})
            record = cursor.fetchall()

            # Ensure username exists and password is correct
            if len(record) != 1 or not check_password_hash(record[0][3], password):
                return flash("invalid username and/or password")

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
        return render_template("signin.html")
