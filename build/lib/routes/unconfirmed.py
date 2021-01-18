import sqlite3
import traceback
import sys
import re

from flask import Blueprint, render_template, redirect, session, request, flash, get_flashed_messages
from application import getUserName, getUserPicture, mail, login_required, getUserEmail, sendPin, getUserPin, getUserTime
from flask_mail import Message, Mail
from time import time

# Set Blueprints
unconfirmed = Blueprint('unconfirmed', __name__,)

@unconfirmed.route("/unconfirmed", methods=["GET", "POST"])
@login_required
def unconfirmedFunction():

    # Force flash() to get the messages on the same page as the redirect.
    get_flashed_messages()
    # Get user email
    email = getUserEmail()
    # Get current time
    now = int(time())
    # Get signup time
    date = getUserTime()
    # Get user PIN
    pin = getUserPin()
    # Get given PIN
    sample = request.form.get("pin")


    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        if request.form.get("confirm"):

            if int(sample) == int(pin) and int(now - date) < 600:

                # Update database with confirmation
                try:

                    sqliteConnection = sqlite3.connect("database.db")
                    cursor = sqliteConnection.cursor()
                    user_id = session["user_id"]
                    status = "True"
                    
                    cursor.execute("UPDATE users SET confirmed=:status WHERE id=:id;", {"status": status, "id": user_id})
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

                return redirect("/")
                
            else:

                flash("Wrong PIN entered and/or PIN timed out.")
                return redirect("/unconfirmed")

                
        if request.form.get("send"):

            sendPin(email)
            flash("An new activation PIN has been sent to your email")

            return redirect("/unconfirmed")

        else:

            return redirect("/unconfirmed")

    else:

        return render_template("unconfirmed.html", name=getUserName(), picture=getUserPicture())