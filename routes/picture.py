import sqlite3
import traceback
import sys

from flask import Blueprint, render_template, redirect, session, request
from application import profileName, uploadPicture, profilePicture

# Set Blueprints
picture = Blueprint('picture', __name__,)

@picture.route("/picture", methods=["GET", "POST"])
def pictureFunction():

    if request.method == "POST":

        if request.files:

            picture = request.files["picture"]
            upload = uploadPicture(picture)

            try:

                sqliteConnection = sqlite3.connect("database.db")
                cursor = sqliteConnection.cursor()
                
                cursor.execute("INSERT INTO users(picture) VALUES (:picture);", {"picture": upload})
                record = sqliteConnection.commit()
                print(record)
 
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
        

        return redirect("/")

    else:

        return render_template("picture.html", name=profileName(), picture=profilePicture())