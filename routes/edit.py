import sqlite3
import traceback
import sys
import re
import os

from flask import Blueprint, render_template, redirect, session, request, flash, get_flashed_messages
from application import getUserName, getUserPicture, login_required, confirmed_required, getUserRole, role_required, uploadPicture, allowed_file
from werkzeug.utils import secure_filename

# Set Blueprints
edit = Blueprint('edit', __name__,)

@edit.route("/edit", methods=["GET", "POST"])
@login_required
@confirmed_required
@role_required
def editFunction():    

    # Force flash() to get the messages on the same page as the redirect.
    get_flashed_messages()

    if request.method == "POST":

        # Get variables
        plant_id = request.form.get("plant_id")
        name = request.form.get("name")
        stock = request.form.get("stock")
        price = request.form.get("price")
        description = request.form.get("description")
        show = request.form.get("show")

        # Convert show value to string
        if show == None:
            show = "No"
        if show == "show":
            show = "Yes"

        # Ensure the plant name was submitted
        if not name:
            flash("must provide plant name")
            return redirect("/edit")

        # Ensure the plant name fits server-side
        if not re.search("^[a-zA-Z0-9]{1,50}$", name):
            flash("Invalid plant name")
            return redirect("/edit")

        # Ensure the plant stock was submitted
        if not stock:
            flash("must provide plant stock")
            return redirect("/edit")

        # Ensure the plant stock fits server-side
        if not re.search("^[0-9]+$", stock):
            flash("Invalid plant stock")
            return redirect("/edit")

        # Ensure the plant price was submitted
        if not stock:
            flash("must provide plant price")
            return redirect("/edit")

        # Ensure the plant price fits server-side
        if not re.search("^[0-9]+$", stock):
            flash("Invalid plant price")
            return redirect("/edit")

        # Ensure the plant description was submitted
        if not description:
            flash("must provide plant description")
            return redirect("/edit")

        # Ensure the plant description fits server-side
        if not re.search("^(?!;).+", description):
            flash("Invalid plant description")
            return redirect("/edit")


        # Update plant name, stock, price, description and show status into the table
        try:

            sqliteConnection = sqlite3.connect("database.db")
            cursor = sqliteConnection.cursor()

            cursor.execute("UPDATE plants SET name=:name, stock=:stock, price=:price, description=:description, show=:show WHERE id=:plant_id;", {"name": name, "stock": stock, "price": price, "description": description, "show": show, "plant_id": plant_id})
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

        if file and allowed_file(file.filename):

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

        flash("Plant edited")
        return redirect("/administration")


    else:

        # Get arguments from url_for in administration
        thisPlant = request.args.getlist("plants")
    
        return render_template("edit.html", name=getUserName(), picture=getUserPicture(), role=getUserRole(), plants=thisPlant)