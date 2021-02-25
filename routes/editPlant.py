import traceback
import sys
import re
import os
import html2text

from flask import Blueprint, render_template, redirect, session, request, flash, get_flashed_messages
from application import getUserName, getUserPicture, login_required, confirmed_required, getUserRole, role_required, uploadPicture, allowed_file, db, Plants, getInputLength
from werkzeug.utils import secure_filename
from flask_sqlalchemy import SQLAlchemy


# Set Blueprints
editPlant = Blueprint('editPlant', __name__,)


@editPlant.route("/editPlant", methods=["GET", "POST"])
@login_required
@confirmed_required
@role_required
def editPlantFunction():    

    # Force flash() to get the messages on the same page as the redirect.
    get_flashed_messages()


    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Get variable
        plant_id = request.form.get("plant_id")
        name = request.form.get("name")
        stock = request.form.get("stock")
        price = request.form.get("price")
        offer = request.form.get("offer")
        length = request.form.get("length")
        width = request.form.get("width")
        height = request.form.get("height")
        weight = request.form.get("weight")
        html = request.form.get("ckeditor")
        description = html2text.html2text(html)
        express = request.form.get("express")
        reduced = request.form.get("reduced")
        show = request.form.get("show")


        # Check length
        getInputLength(name, 100, "Name is too long (100)", "danger", "/editPlant")
        getInputLength(stock, 6, "Stock is too big (6)", "danger", "/editPlant")
        getInputLength(price, 6, "Price is too big (6)", "danger", "/editPlant")
        getInputLength(offer, 6, "Offer is too big (6)", "danger", "/editPlant")
        getInputLength(length, 6, "Length is too big (6)", "danger", "/editPlant")
        getInputLength(width, 6, "Width is too big (6)", "danger", "/editPlant")
        getInputLength(height, 6, "Height is too big (6)", "danger", "/editPlant")
        getInputLength(weight, 6, "Weight is too big (6)", "danger", "/editPlant")
        getInputLength(description, 300, "Description is too long (300)", "danger", "/editPlant")


        # Convert offer value to integer
        if offer == "":
            offer = 0


        # Convert express value to string
        if express == None:
            express = "No"
        if express == "express":
            express = "Yes"


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
            return redirect("/editPlant")


        # Ensure the plant name fits server-side
        if not re.search("^[a-zA-Z 0-9]{1,100}$", name):
            flash("Invalid plant name", "danger")
            return redirect("/editPlant")


        # Ensure the plant stock was submitted
        if not stock:
            flash("must provide plant stock", "warning")
            return redirect("/editPlant")


        # Ensure the plant stock fits server-side
        if not re.search("^[0-9]+$", stock):
            flash("Invalid plant stock", "danger")
            return redirect("/editPlant")


        # Ensure the plant price was submitted
        if not price:
            flash("must provide plant price", "warning")
            return redirect("/editPlant")


        # Ensure the plant price fits server-side
        if not re.search("^[0-9]+\.?[0-9]+$", format(price, ".2f")):
            flash("Invalid plant price", "danger")
            return redirect("/editPlant")


        # Ensure the plant offer fits server-side
        if offer != 0:
            if not re.search("^[0-9]+\.?[0-9]+$", format(offer, ".2f")):
                flash("Invalid plant offer", "danger")
                return redirect("/editPlant")


        # Ensure the plant length was submitted
        if not length:
            flash("must provide plant length", "warning")
            return redirect("/editPlant")


        # Ensure the plant length fits server-side
        if not re.search("^[0-9]+$", length):
            flash("Invalid plant length", "danger")
            return redirect("/editPlant")


        # Ensure the plant width was submitted
        if not width:
            flash("must provide plant width", "warning")
            return redirect("/editPlant")


        # Ensure the plant width fits server-side
        if not re.search("^[0-9]+$", width):
            flash("Invalid plant width", "danger")
            return redirect("/editPlant")


        # Ensure the plant height was submitted
        if not height:
            flash("must provide plant height", "warning")
            return redirect("/editPlant")


        # Ensure the plant height fits server-side
        if not re.search("^[0-9]+$", height):
            flash("Invalid plant height", "danger")
            return redirect("/editPlant")


        # Ensure the plant weight was submitted
        if not weight:
            flash("must provide plant weight", "warning")
            return redirect("/editPlant")


        # Ensure the plant weight fits server-side
        if not re.search("^[0-9]+$", weight):
            flash("Invalid plant weight", "danger")
            return redirect("/editPlant")


        # Ensure the plant description was submitted
        if not description:
            flash("must provide plant description", "warning")
            return redirect("/editPlant")


        # Ensure the plant description fits server-side
        if not re.search("^(?!;).+", description):
            flash("Invalid plant description", "danger")
            return redirect("/editPlant")


        # Update plant name, stock, price, description and show status into the table and commit
        query = Plants.query.filter_by(id=plant_id).first()
        query.name = name
        query.stock = stock
        query.price = price
        query.offer = offer
        query.length = length
        query.width = width
        query.height = height
        query.weight = weight
        query.description = description
        query.express = express
        query.reduced = reduced
        query.show = show
        db.session.commit()


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
        flash("Plant edited", "success")
        return redirect("/administration")


    else:

        # Get arguments from url_for in administration
        thisPlant = request.args.getlist("plants")

    
        return render_template("editPlant.html", name=getUserName(), picture=getUserPicture(), role=getUserRole(), plants=thisPlant)