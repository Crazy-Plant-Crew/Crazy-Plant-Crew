import sqlite3
import traceback
import sys

from flask import Blueprint, render_template, redirect, session, request


# Set Blueprints
message = Blueprint('message', __name__,)

@message.route("/message", methods=["GET", "POST"])
def messageFunction():

    if request.method == "POST":

        print("message")

    else:

        # get the username to access profile menu
        try:

            sqliteConnection = sqlite3.connect("database.db")
            cursor = sqliteConnection.cursor()

            # Check who's id is logged in
            loggedId = session["user_id"]
            
            # Query database for username
            cursor.execute("SELECT username FROM users WHERE id=:id", {"id": loggedId})
            name = cursor.fetchall()[0][0]

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

    
    return render_template("message.html", name=name)