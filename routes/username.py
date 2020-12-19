import sqlite3
import traceback
import sys

from flask import Blueprint, render_template, redirect, session, request, flash
from application import profileName, profilePicture

# Set Blueprints
username = Blueprint('username', __name__,)

@username.route("/username", methods=["GET", "POST"])
def usernameFunction():

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        username = request.form.get("username")

        # Ensure username was submitted
        if not username:
            return flash("must provide username")

        # Query database for username if already exists
        try:

            sqliteConnection = sqlite3.connect("database.db")
            cursor = sqliteConnection.cursor()
            user_id = session["user_id"]
            
            # Query database for username
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