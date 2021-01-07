import sqlite3
import traceback
import sys

from flask import Blueprint, render_template, redirect, session, request, flash, get_flashed_messages
from application import getUserName, getUserPicture, login_required, confirmed_required, getUserRole

# Set Blueprints
mailing = Blueprint('mailing', __name__,)

@mailing.route("/mailing", methods=["GET", "POST"])
@login_required
@confirmed_required
def mailingFunction():   

    # Force flash() to get the messages on the same page as the redirect.
    get_flashed_messages() 

    if request.method == "POST":

        if request.form.get('activate'):

            # Update database with newsletter preference
            try:

                sqliteConnection = sqlite3.connect("database.db")
                cursor = sqliteConnection.cursor()
                user_id = session["user_id"]
                newsletter = "True"
                
                # Update database with newsletter
                cursor.execute("UPDATE users SET newsletter=:newsletter WHERE id=:user_id;", {"newsletter": newsletter, "user_id": user_id})
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

        if request.form.get('deactivate'):

            # Update database with newsletter preference
            try:

                sqliteConnection = sqlite3.connect("database.db")
                cursor = sqliteConnection.cursor()
                user_id = session["user_id"]
                newsletter = "False"
                
                # Update database with newsletter
                cursor.execute("UPDATE users SET newsletter=:newsletter WHERE id=:user_id;", {"newsletter": newsletter, "user_id": user_id})
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
            
        flash("Newsletter updated")
        return redirect("/profile")

    else:
    
        return render_template("mailing.html", name=getUserName(), picture=getUserPicture(), role=getUserRole())