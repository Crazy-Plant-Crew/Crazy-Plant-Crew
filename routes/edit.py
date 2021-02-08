import traceback
import sys
import re
import os
import html2text

from flask import Blueprint, render_template, redirect, session, request, flash, get_flashed_messages
from application import getUserName, getUserPicture, login_required, confirmed_required, getUserRole, role_required, uploadPicture, allowed_file, db, Plants
from werkzeug.utils import secure_filename
from flask_sqlalchemy import SQLAlchemy


# Set Blueprints
edit = Blueprint('edit', __name__,)


@edit.route("/edit", methods=["GET", "POST"])
@login_required
@confirmed_required
@role_required
def editFunction():    

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
        html = request.form.get("ckeditor")
        description = html2text.html2text(html)
        reduced = request.form.get("reduced")
        show = request.form.get("show")


        # Convert show value to string
        if show == None:
            show = "No"
        if show == "show":
            show = "Yes"


        # Ensure the plant name was submitted
        if not name:
            flash("must provide plant name", "warning")
            return redirect("/edit")


        # Ensure the plant name fits server-side
        if not re.search("^[a-zA-Z0-9]{1,50}$", name):
            flash("Invalid plant name", "danger")
            return redirect("/edit")


        # Ensure the plant stock was submitted
        if not stock:
            flash("must provide plant stock", "warning")
            return redirect("/edit")


        # Ensure the plant stock fits server-side
        if not re.search("^[0-9]+$", stock):
            flash("Invalid plant stock", "danger")
            return redirect("/edit")


        # Ensure the plant price was submitted
        if not price:
            flash("must provide plant price", "warning")
            return redirect("/edit")


        # Ensure the plant price fits server-side
        if not re.search("^[0-9]+$", price):
            flash("Invalid plant price", "danger")
            return redirect("/edit")


        # Ensure the plant offer fits server-side
        if offer not None:
            if not re.search("^[0-9]+$", offer):
                flash("Invalid plant offer", "danger")
                return redirect("/edit")


        # Ensure the plant description was submitted
        if not description:
            flash("must provide plant description", "warning")
            return redirect("/edit")


        # Ensure the plant description fits server-side
        if not re.search("^(?!;).+", description):
            flash("Invalid plant description", "danger")
            return redirect("/edit")


        # Update plant name, stock, price, description and show status into the table and commit
        query = Plants.query.filter_by(id=plant_id).first()
        query.name = name
        query.stock = stock
        query.price = price
        query.offer = offer
        query.description = description
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

    
        return render_template("edit.html", name=getUserName(), picture=getUserPicture(), role=getUserRole(), plants=thisPlant)