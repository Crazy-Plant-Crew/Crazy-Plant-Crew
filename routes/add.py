import traceback
import sys
import re
import os

from flask import Blueprint, render_template, redirect, session, request, flash, get_flashed_messages
from application import getUserName, getUserPicture, login_required, confirmed_required, getUserRole, role_required, uploadPicture, allowed_file, db, Plants, getInputLength
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
        offer = request.form.get("offer")
        description = request.form.get("ckeditor")
        reduced = request.form.get("reduced")
        show = request.form.get("show")


        # Check length
        getInputLength(name, 100, "Name is too long (100)", "danger", "/add")
        getInputLength(stock, 6, "Stock is too long (6)", "danger", "/add")
        getInputLength(price, 6, "Price is too long (6)", "danger", "/add")
        getInputLength(offer, 6, "Offer is too long (6)", "danger", "/add")
        getInputLength(description, 300, "Description is too long (300)", "danger", "/add")


        # Convert offer value to integer
        if offer == "":
            offer = 0


        # Convert show value to string
        if show == None:
            show = "No"
        if show == "show":
            show = "Yes"

        
        # Convert reduced value to string
        if reduced == None:
            reduced = "No"
        if reduced == "reduced":
            reduced = "Yes"


        # Ensure the plant name was submitted
        if not name:
            flash("must provide plant name", "warning")
            return redirect("/add")


        # Ensure the plant name fits server-side
        if not re.search("^[a-zA-Z0-9]{1,50}$", name):
            flash("Invalid plant name", "danger")
            return redirect("/add")


        # Ensure the plant stock was submitted
        if not stock:
            flash("must provide plant stock", "warning")
            return redirect("/add")


        # Ensure the plant stock fits server-side
        if not re.search("^[0-9]+$", stock):
            flash("Invalid plant stock", "danger")
            return redirect("/add")


        # Ensure the plant price was submitted
        if not price:
            flash("must provide plant price", "warning")
            return redirect("/add")


        # Ensure the plant price fits server-side
        if not re.search("^[0-9]+$", price):
            flash("Invalid plant price", "danger")
            return redirect("/add")


        # Ensure the plant offer fits server-side
        if offer != 0:
            if not re.search("^[0-9]+$", offer):
                flash("Invalid plant offer", "danger")
                return redirect("/add")


        # Ensure the plant description was submitted
        if not description:
            flash("must provide plant description", "warning")
            return redirect("/add")


        # Ensure the plant description fits server-side
        if not re.search("^(?!;).+", description):
            flash("Invalid plant description", "danger")
            return redirect("/add")


        # Insert plant name, stock, price, description and show status into the table
        db.session.add(Plants(name=name, stock=stock, price=price, offer=offer, description=description, reduced=reduced, show=show))
        db.session.commit()


        # Query database for id of the last entered plant
        query = Plants.query.all()
        plant_id = query[-1].id


        # Save, upload and delete picture file
        file1 = request.files["picture"]
        if file1 and allowed_file(file1.filename):

            filename = secure_filename(file1.filename)
            file1.save(os.path.join("./static", filename))
            upload = uploadPicture("./static/" + filename)
            os.remove("./static/" + filename)

            # Update database with new image url 
            query = Plants.query.filter_by(id=plant_id).first()
            query.picture = upload
            db.session.commit()


        # Save, upload and delete first thumbnail file
        file2 = request.files["thumbnail1"]
        if file2 and allowed_file(file2.filename):

            filename = secure_filename(file2.filename)
            file2.save(os.path.join("./static", filename))
            upload = uploadPicture("./static/" + filename)
            os.remove("./static/" + filename)

            # Update database with new image url 
            query = Plants.query.filter_by(id=plant_id).first()
            query.thumbnail1 = upload
            db.session.commit()


        # Save, upload and delete second thumbnail file
        file3 = request.files["thumbnail2"]
        if file3 and allowed_file(file3.filename):

            filename = secure_filename(file3.filename)
            file3.save(os.path.join("./static", filename))
            upload = uploadPicture("./static/" + filename)
            os.remove("./static/" + filename)

            # Update database with new image url 
            query = Plants.query.filter_by(id=plant_id).first()
            query.thumbnail2 = upload
            db.session.commit()


        # Flash result & redirect
        flash("Plant added", "success")
        return redirect("/administration")


    else:
    
        return render_template("add.html", name=getUserName(), picture=getUserPicture(), role=getUserRole())