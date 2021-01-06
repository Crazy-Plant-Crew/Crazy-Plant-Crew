import sqlite3
import traceback
import sys

from flask import Blueprint, render_template, redirect, session, request, flash, get_flashed_messages
from application import getUserName, getUserPicture, login_required, confirmed_required, getUserRole, role_required, sendMail
from flask_mail import Message, Mail

# Set Blueprints
newsletter = Blueprint('newsletter', __name__,)

@newsletter.route("/newsletter", methods=["GET", "POST"])
@login_required
@confirmed_required
@role_required
def newsletterFunction():

    # Force flash() to get the messages on the same page as the redirect.
    get_flashed_messages()


    if request.method == "POST":

        # Get variables
        subject = request.form.get("subject")
        body = request.form.get("body")
        address = request.form.get("address")
        newsletter = request.form.get("newsletter")

        # Query database for user emails for newsletter 
        try:

            sqliteConnection = sqlite3.connect("database.db")
            cursor = sqliteConnection.cursor()
            status = "True"
            
            # Query database
            cursor.execute("SELECT email FROM users WHERE newsletter=:newsletter;", {"newsletter": status})
            email = cursor.fetchall()

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


        if address != "" and newsletter == None:

            # Send email (subject, email, body)
            sendMail(subject, address, body)
            flash("Single email sent")

        elif address == "" and newsletter == newsletter:

            # Loop through email list and send 
            index  = 0
            while index < len(email):
                sendMail(subject, email[index][0], body)
                index += 1
            flash("Group email sent")

        else:

            flash("Error: either to one address or select Newsletter and leave address blank")
            return redirect("/newsletter")

        return redirect("/")
    
    else:

        return render_template("newsletter.html", name=getUserName(), picture=getUserPicture(), role=getUserRole())