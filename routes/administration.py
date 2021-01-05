import sqlite3
import traceback
import sys

from flask import Blueprint, render_template, redirect, session, request, flash, get_flashed_messages, url_for
from application import getUserName, getUserPicture, login_required, confirmed_required, role_required, getUserRole

# Set Blueprints
administration = Blueprint('administration', __name__,)

@administration.route("/administration", methods=["GET", "POST"])
@login_required
@confirmed_required
@role_required
def administrationFunction():

    # Force flash() to get the messages on the same page as the redirect.
    get_flashed_messages()

    # Query database for plants
    try:

        sqliteConnection = sqlite3.connect("database.db")
        cursor = sqliteConnection.cursor()
        
        # Query database
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


    if request.method == "POST":

        if "delete" in request.form:
        
            # Loop through the record list to match plant ID when delete button is pressed
            index = 0
            while index < len(record):

                if int(request.form["delete"]) == int(record[index][0]):

                    # Query database for plant id to delete row
                    try:

                        sqliteConnection = sqlite3.connect("database.db")
                        cursor = sqliteConnection.cursor()
                        plant_id = record[index][0]
                        
                        cursor.execute("DELETE FROM plants WHERE id=:id;", {"id": plant_id})
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

                    flash("Plant deleted")
                    return redirect("/administration")

                else:

                    index += 1


        if "edit" in request.form:   

            # Loop through the record list to match plant ID when edit button is pressed
            index = 0
            while index < len(record):

                if int(request.form["edit"]) == int(record[index][0]):

                    thisPlant = record[index]

                    return redirect(url_for("edit.editFunction", plants=thisPlant))

                else:

                    index += 1

    else:
   
        return render_template("administration.html", name=getUserName(), picture=getUserPicture(), role=getUserRole(), plants=record)