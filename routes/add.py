import traceback
import sys
import re
import os

from flask import Blueprint, render_template, redirect, session, request, flash, get_flashed_messages
from application import getUserName, getUserPicture, login_required, confirmed_required, getUserRole, role_required, uploadPicture, allowed_file, db, Plants
from werkzeug.utils import secure_filename
from flask_sqlalchemy import SQLAlchemy


# Set Blueprints
add = Blueprint('add', __name__,)


@add.route("/add", methods=["GET", "POST"])
@login_required
@confirmed_required
@role_required
def addFunction():

    # Force flash() to get the messages on the same page as the redirect.
    get_flashed_messages()


    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Get variable
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


        # Insert plant name, stock, price, description and show status into the table
        db.session.add(Plants(name=name, stock=stock, price=price, description=description, show=show))
        db.session.commit()


        # Query database for plant if already exists so the last is selected as the last plant is the one just added
        query = Plants.query.filter(name=name).all()

        if len(query) != 1:
            plant_id = query[-1].id

        else:
            plant_id = query.id


        # Save, upload and delete picture file
        file = request.files["picture"]
        if file and allowed_file(file.filename):

            filename = secure_filename(file.filename)
            file.save(os.path.join("./static", filename))
            upload = uploadPicture("./static/" + filename)
            os.remove("./static/" + filename)

            # Update database with new image url 
            query = Plants.query.filter_by(id=plant_id).first()
            query.picture = upload
            db.session.commit()


        # Flash result & redirect
        flash("Plant added")
        return redirect("/administration")


    else:
    
        return render_template("add.html", name=getUserName(), picture=getUserPicture(), role=getUserRole())