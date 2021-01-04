import sqlite3
import traceback
import sys

from flask import Blueprint, render_template, redirect, session, request
from application import getUserName, getUserPicture, login_required, confirmed_required, getUserRole

# Set Blueprints
delete = Blueprint('delete', __name__,)

@delete.route("/delete", methods=["GET", "POST"])
@login_required
@confirmed_required
def emailFunction():

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Query database for user id to delete it 
        try:

            sqliteConnection = sqlite3.connect("database.db")
            cursor = sqliteConnection.cursor()
            user_id = session["user_id"]
            
            cursor.execute("DELETE FROM users WHERE id=:user_id;", {"user_id": user_id})
            sqliteConnection.commit()

            session.clear()

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

        return redirect("/signin")

    else:

        return render_template("delete.html", name=getUserName(), picture=getUserPicture(), role=getUserRole())