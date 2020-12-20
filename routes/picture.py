import sqlite3
import traceback
import sys
import os

from flask import Blueprint, render_template, redirect, session, request, flash
from application import profileName, uploadPicture, profilePicture
from werkzeug.utils import secure_filename

# Set Blueprints
picture = Blueprint('picture', __name__,)

@picture.route("/picture", methods=["GET", "POST"])
def pictureFunction():

    if request.method == "POST":

        # check if the post request has the file part
        if "picture" not in request.files:
            flash("No file part")
            return redirect("/picture")

        file = request.files["picture"]

        # if user does not select file, browser also submit a empty part without filename
        if file.filename == "":
            flash("No selected file")
            return redirect("/picture")

        # Check if all conditions are satisfied
        if file and file.filename:
            filename = secure_filename(file.filename)
            file.save(os.path.join("./static", filename))
            upload = uploadPicture("./static/" + filename)          

        # Update database with new image url 
        try:

            sqliteConnection = sqlite3.connect("database.db")
            cursor = sqliteConnection.cursor()
            user_id = session["user_id"]
            
            cursor.execute("UPDATE users SET picture=:picture WHERE id=:user_id;", {"picture": upload, "user_id": user_id})
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

        return redirect("/")

    else:

        return render_template("picture.html", name=profileName(), picture=profilePicture())