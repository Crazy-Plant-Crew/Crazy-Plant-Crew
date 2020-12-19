import sqlite3
import traceback
import sys

from flask import Blueprint, render_template, redirect, session, request, flash
from werkzeug.security import check_password_hash, generate_password_hash
from application import profileName, profilePicture

# Set Blueprints
password = Blueprint('password', __name__,)

@password.route("/password", methods=["GET", "POST"])
def passwordFunction():

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        password = request.form.get("password")

        # Ensure password was submitted
        if not password:
            return flash("must provide password")

        # Query database for password if already exists
        try:

            sqliteConnection = sqlite3.connect("database.db")
            cursor = sqliteConnection.cursor()
            user_id = session["user_id"]
            
            # Query database for password
            cursor.execute("UPDATE users SET hash=:hash WHERE id=:user_id;", {"hash": generate_password_hash(password), "user_id": user_id})
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

    return render_template("password.html", name=profileName(), picture=profilePicture())