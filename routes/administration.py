import sqlite3
import traceback
import sys

from flask import Blueprint, render_template, redirect, session, request
from application import getUserName, getUserPicture, login_required, confirmed_required, role_required, getUserRole

# Set Blueprints
administration = Blueprint('administration', __name__,)

@administration.route("/administration", methods=["GET", "POST"])
@login_required
@confirmed_required
@role_required
def administrationFunction():    

    if request.method == "POST":

        print("administration")

    else:

        # Query database for username if already exists
        try:

            sqliteConnection = sqlite3.connect("database.db")
            cursor = sqliteConnection.cursor()
            
            # Query database for username
            cursor.execute("SELECT * FROM plants;")
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

    
        return render_template("administration.html", name=getUserName(), picture=getUserPicture(), role=getUserRole(), plants=record)