import sqlite3
import traceback
import sys
import re
import os

from flask import Blueprint, render_template, redirect, session, request, flash, get_flashed_messages
from application import getUserName, getUserPicture, login_required, confirmed_required, getUserRole, role_required, uploadPicture, allowed_file
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

        # Get variables
        name = request.form.get("name")
        stock = request.form.get("stock")
        price = request.form.get("price")
        description = request.form.get("ckeditor")
        show = request.form.get("show")

        # Convert show value to string
        if show == None:
            show = "No"
        if show == "show":
            show = "Yes"

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

        # Ensure the plant price was submitted
        if not stock:
            flash("must provide plant price")
            return redirect("/add")

        # Ensure the plant price fits server-side
        if not re.search("^[0-9]+$", stock):
            flash("Invalid plant price")
            return redirect("/add")

        # Ensure the plant description was submitted
        if not description:
            flash("must provide plant description")
            return redirect("/add")

        # Ensure the plant description fits server-side
        if not re.search("^(?!;).+", description):
            flash("Invalid plant description")
            return redirect("/add")


        # Insert plant name, stock, description and show status into the table
        try:

            sqliteConnection = sqlite3.connect("database.db")
            cursor = sqliteConnection.cursor()
            
            cursor.execute("INSERT INTO plants(name, stock, price, description, show) VALUES (:name, :stock, :price, :description, :show)", {"name": name, "stock": stock, "price": price, "description": description, "show": show})
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


        # Query database for plant if already exists so the last is selected
        try:

            sqliteConnection = sqlite3.connect("database.db")
            cursor = sqliteConnection.cursor()
            
            # Query database for plant name
            cursor.execute("SELECT * FROM plants WHERE name=:name;", {"name": name})
            record = cursor.fetchall()

            # Check if plant name is free
            if len(record) != 1:
                plant_id = record[-1][0]
            else:
                plant_id = record[0][0]

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

        if file and allowed_file(file.filename):

            filename = secure_filename(file.filename)
            file.save(os.path.join("./static", filename))
            upload = uploadPicture("./static/" + filename)
            os.remove("./static/" + filename)

            # Update database with new image url 
            try:

                sqliteConnection = sqlite3.connect("database.db")
                cursor = sqliteConnection.cursor()
                
                cursor.execute("UPDATE plants SET picture=:picture WHERE id=:id;", {"picture": upload, "id": plant_id})
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