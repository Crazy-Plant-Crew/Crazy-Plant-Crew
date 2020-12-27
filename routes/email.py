import sqlite3
import traceback
import sys

from flask import Blueprint, render_template, redirect, session, request, flash
from application import profileName, profilePicture

# Set Blueprints
email = Blueprint('email', __name__,)

@email.route("/email", methods=["GET", "POST"])
def emailFunction():

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        email = request.form.get("email")

        # Ensure email was submitted
        if not email:
            return flash("must provide email")

        # Query database for email if already exists
        try:

            sqliteConnection = sqlite3.connect("database.db")
            cursor = sqliteConnection.cursor()
            user_id = session["user_id"]
            
            # Query database for email
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