import sqlite3
import traceback
import sys

from flask import Blueprint, render_template, redirect, session, request, flash, get_flashed_messages
from application import getUserName, getUserPicture, login_required, confirmed_required, getUserRole, role_required

# Set Blueprints
basket = Blueprint('basket', __name__,)

@basket.route("/basket", methods=["GET", "POST"])
@login_required
@confirmed_required
def basketFunction():    

    # Force flash() to get the messages on the same page as the redirect.
    get_flashed_messages()


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


    if request.method == "POST":

        if "delete" in request.form:
        
            # Loop through the record list to match plant ID when delete button is pressed
            index = 0
            while index < len(baskets):

                if int(request.form["delete"]) == int(baskets[index][0]):

                    # Query database for plant id to delete row
                    try:

                        sqliteConnection = sqlite3.connect("database.db")
                        cursor = sqliteConnection.cursor()
                        basket_id = baskets[index][0]
                        
                        cursor.execute("DELETE FROM baskets WHERE id=:id;", {"id": basket_id})
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

                    flash("Item deleted")
                    return redirect("/basket")

                else:

                    index += 1


    else:

        index = 0
        total = 0
        while index < len(baskets):

            total += baskets[index][7]
            index += 1
    
        return render_template("basket.html", name=getUserName(), picture=getUserPicture(), role=getUserRole(), baskets=baskets, total=int(total))