import sqlite3
import traceback
import sys

from flask import Blueprint, render_template, redirect, session, request, flash, get_flashed_messages, url_for
from application import getUserName, getUserPicture, login_required, confirmed_required, getUserRole, role_required

# Set Blueprints
communication = Blueprint('communication', __name__,)

@communication.route("/communication", methods=["GET", "POST"])
@login_required
@confirmed_required
@role_required
def communicationFunction():

    # Force flash() to get the messages on the same page as the redirect.
    get_flashed_messages()  

    # Query database for news to display them
    try:

        sqliteConnection = sqlite3.connect("database.db")
        cursor = sqliteConnection.cursor()
        
        # Query database
        cursor.execute("SELECT * FROM news;")
        communications = cursor.fetchall()

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

        if "erase" in request.form:
        
            # Loop through the record list to match plant ID when delete button is pressed
            index = 0
            while index < len(communications):

                if int(request.form["erase"]) == int(communications[index][0]):

                    # Query database for plant id to delete row
                    try:

                        sqliteConnection = sqlite3.connect("database.db")
                        cursor = sqliteConnection.cursor()
                        news_id = communications[index][0]
                        
                        cursor.execute("DELETE FROM news WHERE id=:id;", {"id": news_id})
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

                    flash("News deleted")
                    return redirect("/communication")

                else:

                    index += 1


        if "change" in request.form:   

            # Loop through the record list to match plant ID when edit button is pressed
            index = 0
            while index < len(communications):

                if int(request.form["change"]) == int(communications[index][0]):

                    thisNews = communications[index]

                    return redirect(url_for("change.changeFunction", news=thisNews))

                else:

                    index += 1

        return redirect("/")


    else:
    
        return render_template("communication.html", name=getUserName(), picture=getUserPicture(), role=getUserRole(), communications=communications)