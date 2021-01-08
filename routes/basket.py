import sqlite3
import traceback
import sys

from flask import Blueprint, render_template, redirect, session, request
from application import getUserName, getUserPicture, login_required, confirmed_required, getUserRole, role_required

# Set Blueprints
basket = Blueprint('basket', __name__,)

@basket.route("/basket", methods=["GET", "POST"])
@login_required
@confirmed_required
def basketFunction():    

    if request.method == "POST":

        print("basket")

    else:

        # Query database for plants to display them
        try:

            sqliteConnection = sqlite3.connect("database.db")
            cursor = sqliteConnection.cursor()

            # Set correct status for query
            status = "Yes"
            
            # Query database
            cursor.execute("SELECT * FROM plants WHERE show=:show;", {"show": status})
            plants = cursor.fetchall()

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



        # Query database for baskets item
        try:

            sqliteConnection = sqlite3.connect("database.db")
            cursor = sqliteConnection.cursor()
            
            # Query database
            cursor.execute("SELECT * FROM baskets;")
            baskets = cursor.fetchall()

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

    
        return render_template("basket.html", name=getUserName(), picture=getUserPicture(), role=getUserRole(), baskets=baskets, plants=plants)