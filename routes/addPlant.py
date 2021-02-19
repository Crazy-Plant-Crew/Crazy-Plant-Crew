import traceback
import sys
import re
import os

from flask import Blueprint, render_template, redirect, session, request, flash, get_flashed_messages
from application import getUserName, getUserPicture, login_required, confirmed_required, getUserRole, role_required, uploadPicture, allowed_file, db, Plants, getInputLength
from werkzeug.utils import secure_filename
from flask_sqlalchemy import SQLAlchemy


# Set Blueprints
addPlant = Blueprint('addPlant', __name__,)


@addPlant.route("/addPlant", methods=["GET", "POST"])
@login_required
@confirmed_required
@role_required
def addPlantFunction():

    # Force flash() to get the messages on the same page as the redirect.
    get_flashed_messages()


    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Get variable
        name = request.form.get("name")
        stock = request.form.get("stock")
        price = request.form.get("price")
        offer = request.form.get("offer")
        length = request.form.get("length")
        width = request.form.get("width")
        height = request.form.get("height")
        weight = request.form.get("weight")
        description = request.form.get("ckeditor")
        reduced = request.form.get("reduced")
        show = request.form.get("show")


        # Check length
        getInputLength(name, 100, "Name is too long (100)", "danger", "/addPlant")
        getInputLength(stock, 6, "Stock is too big (6)", "danger", "/addPlant")
        getInputLength(price, 6, "Price is too big (6)", "danger", "/addPlant")
        getInputLength(offer, 6, "Offer is too big (6)", "danger", "/addPlant")
        getInputLength(length, 6, "Length is too big (6)", "danger", "/addPlant")
        getInputLength(width, 6, "Width is too big (6)", "danger", "/addPlant")
        getInputLength(height, 6, "Height is too big (6)", "danger", "/addPlant")
        getInputLength(weight, 6, "Weight is too big (6)", "danger", "/addPlant")
        getInputLength(description, 300, "Description is too long (300)", "danger", "/addPlant")


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
            return redirect("/addPlant")


        # Ensure the plant name fits server-side
        if not re.search("^[a-zA-Z 0-9]{1,100}$", name):
            flash("Invalid plant name", "danger")
            return redirect("/addPlant")


        # Ensure the plant stock was submitted
        if not stock:
            flash("must provide plant stock", "warning")
            return redirect("/addPlant")


        # Ensure the plant stock fits server-side
        if not re.search("^[0-9]+$", stock):
            flash("Invalid plant stock", "danger")
            return redirect("/addPlant")


        # Ensure the plant price was submitted
        if not price:
            flash("must provide plant price", "warning")
            return redirect("/addPlant")


        # Ensure the plant price fits server-side
        if not re.search("^[0-9]+$", price):
            flash("Invalid plant price", "danger")
            return redirect("/addPlant")


        # Ensure the plant offer fits server-side
        if offer != 0:
            if not re.search("^[0-9]+$", offer):
                flash("Invalid plant offer", "danger")
                return redirect("/addPlant")


        # Ensure the plant length was submitted
        if not length:
            flash("must provide plant length", "warning")
            return redirect("/addPlant")


        # Ensure the plant length fits server-side
        if not re.search("^[0-9]+$", length):
            flash("Invalid plant length", "danger")
            return redirect("/addPlant")


        # Ensure the plant width was submitted
        if not width:
            flash("must provide plant width", "warning")
            return redirect("/addPlant")


        # Ensure the plant width fits server-side
        if not re.search("^[0-9]+$", width):
            flash("Invalid plant width", "danger")
            return redirect("/addPlant")


        # Ensure the plant height was submitted
        if not height:
            flash("must provide plant height", "warning")
            return redirect("/addPlant")


        # Ensure the plant height fits server-side
        if not re.search("^[0-9]+$", height):
            flash("Invalid plant height", "danger")
            return redirect("/addPlant")


        # Ensure the plant weight was submitted
        if not weight:
            flash("must provide plant weight", "warning")
            return redirect("/addPlant")


        # Ensure the plant weight fits server-side
        if not re.search("^[0-9]+$", weight):
            flash("Invalid plant weight", "danger")
            return redirect("/addPlant")


        # Ensure the plant description was submitted
        if not description:
            flash("must provide plant description", "warning")
            return redirect("/addPlant")


        # Ensure the plant description fits server-side
        if not re.search("^(?!;).+", description):
            flash("Invalid plant description", "danger")
            return redirect("/addPlant")


        # Insert plant name, stock, price, description and show status into the table
        db.session.add(Plants(name=name, stock=stock, price=price, offer=offer, length=length, width=width, height=height, weight=weight, description=description, reduced=reduced, show=show))
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
    
        return render_template("addPlant.html", name=getUserName(), picture=getUserPicture(), role=getUserRole())