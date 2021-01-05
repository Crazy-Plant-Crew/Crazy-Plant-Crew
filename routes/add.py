import sqlite3
import traceback
import sys
import re
import os

from flask import Blueprint, render_template, redirect, session, request, flash, get_flashed_messages
from application import getUserName, getUserPicture, login_required, confirmed_required, getUserRole, role_required, uploadPicture
from werkzeug.utils import secure_filename

# Set Blueprints
add = Blueprint('add', __name__,)

@add.route("/add", methods=["GET", "POST"])
@login_required
@confirmed_required
@role_required
def addFunction():

    # Force flash() to get the messages on the same page as the redirect.
    get_flashed_messages()

    if request.method == "POST":

        name = request.form.get("name")
        stock = request.form.get("stock")
        description = request.form.get("description")

        # Ensure the plant name was submitted
        if not name:
            flash("must provide plant name")
            return redirect("/add")

        # Ensure the plant name fits server-side
        if not re.search("^[a-zA-Z0-9]{1,50}$", name):
            flash("Invalid plant name")
            return redirect("/add")

        # Ensure the plant stock was submitted
        if not stock:
            flash("must provide plant stock")
            return redirect("/add")

        # Ensure the plant stock fits server-side
        if not re.search("^[0-9]+$", stock):
            flash("Invalid plant stock")
            return redirect("/add")

        # Ensure the plant description was submitted
        if not description:
            flash("must provide plant description")
            return redirect("/add")

        # Ensure the plant description fits server-side
        if not re.search("^(?!;).+", description):
            flash("Invalid plant description")
            return redirect("/add")

        # Check show status
        show = "show" in request.form
        if show == False:
            show = "no"
        else:
            show = "yes"


        # Insert plant name, stock, description and show status into the table
        try:

            sqliteConnection = sqlite3.connect("database.db")
            cursor = sqliteConnection.cursor()
            
            cursor.execute("INSERT INTO plants(name, stock, description, show) VALUES (:name, :stock, :description, :show)", {"name": name, "stock": stock, "description": description, "show": show})
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

        # Save, upload and delete picture file
        file = request.files["picture"]

        if file and file.filename:

            filename = secure_filename(file.filename)
            file.save(os.path.join("./static", filename))
            upload = uploadPicture("./static/" + filename)
            os.remove("./static/" + filename)

            # Update database with new image url 
            try:

                sqliteConnection = sqlite3.connect("database.db")
                cursor = sqliteConnection.cursor()
                
                cursor.execute("UPDATE plants SET picture=:picture WHERE name=:name;", {"picture": upload, "name": name})
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

        flash("Plant added")
        return redirect("/administration")


    # User reached route via GET (as by clicking a link or via redirect)
    else:
    
        return render_template("add.html", name=getUserName(), picture=getUserPicture(), role=getUserRole())