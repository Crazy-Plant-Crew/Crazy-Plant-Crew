import sqlite3
import traceback
import sys

from flask import Blueprint, render_template, redirect, session, request, flash, get_flashed_messages
from application import getUserName, getUserPicture, getUserRole, login_required, confirmed_required

# Set Blueprints
index = Blueprint('index', __name__,)

@index.route("/", methods=["GET", "POST"])
@login_required
@confirmed_required
def indexFunction():

    # Force flash() to get the messages on the same page as the redirect.
    get_flashed_messages()

    # Query database for plants
    try:

        sqliteConnection = sqlite3.connect("database.db")
        cursor = sqliteConnection.cursor()
        status = "Yes"
        
        # Query database
        cursor.execute("SELECT * FROM plants WHERE show=:show;", {"show": status})
        record = cursor.fetchall()

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

    return render_template("index.html", name=getUserName(), picture=getUserPicture(), role=getUserRole(), plants=record)