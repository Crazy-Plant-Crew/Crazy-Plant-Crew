import traceback
import sys
import re

from flask import Blueprint, render_template, redirect, session, request, flash, get_flashed_messages
from application import getUserName, getUserPicture, login_required, confirmed_required, getUserRole, role_required, db, Boxes, getInputLength
from flask_sqlalchemy import SQLAlchemy


# Set Blueprints
editBox = Blueprint('editBox', __name__,)


@editBox.route("/editBox", methods=["GET", "POST"])
@login_required
@confirmed_required
@role_required
def editBoxFunction():    

    # Force flash() to get the messages on the same page as the redirect.
    get_flashed_messages()


    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Get variable
        box_id = request.form.get("box_id")
        name = request.form.get("name")
        length = request.form.get("length")
        width = request.form.get("width")
        height = request.form.get("height")
        price_de = request.form.get("length")
        price_eu = request.form.get("width")
        price_ex = request.form.get("height")


        # Check length
        getInputLength(name, 100, "Name is too long (100)", "danger", "/editBox")
        getInputLength(length, 6, "Length is too big (6)", "danger", "/editBox")
        getInputLength(width, 6, "Price is too big (6)", "danger", "/editBox")
        getInputLength(height, 6, "Offer is too big (6)", "danger", "/editBox")
        getInputLength(price_de, 6, "Length is too big (6)", "danger", "/editBox")
        getInputLength(price_eu, 6, "Width is too big (6)", "danger", "/editBox")
        getInputLength(price_ex, 6, "Height is too big (6)", "danger", "/editBox")


        # Ensure the box name was submitted
        if not name:
            flash("must provide box name", "warning")
            return redirect("/editBox")


        # Ensure the box name fits server-side
        if not re.search("^[a-zA-Z 0-9]{1,100}$", name):
            flash("Invalid plant name", "danger")
            return redirect("/editBox")


        # Ensure the box length was submitted
        if not length:
            flash("must provide box length", "warning")
            return redirect("/editBox")


        # Ensure the box length fits server-side
        if not re.search("^[0-9]+$", length):
            flash("Invalid box length", "danger")
            return redirect("/editBox")


        # Ensure the box width was submitted
        if not width:
            flash("must provide box width", "warning")
            return redirect("/editBox")


        # Ensure the box width fits server-side
        if not re.search("^[0-9]+$", width):
            flash("Invalid box width", "danger")
            return redirect("/editBox")


        # Ensure the box height was submitted
        if not height:
            flash("must provide box height", "warning")
            return redirect("/editBox")


        # Ensure the box height fits server-side
        if not re.search("^[0-9]+$", height):
            flash("Invalid box height", "danger")
            return redirect("/editBox")


        # Ensure the box price in DE was submitted
        if not price_de:
            flash("must provide box price in DE", "warning")
            return redirect("/editBox")


        # Ensure the box price in DE fits server-side
        if not re.search("^[0-9]+\.?[0-9]+$", price_de):
            flash("Invalid box price in DE", "danger")
            return redirect("/editBox")


        # Ensure the box price in EU was submitted
        if not price_eu:
            flash("must provide box price in EU", "warning")
            return redirect("/editBox")


        # Ensure the box price in EU fits server-side
        if not re.search("^[0-9]+\.?[0-9]+$", price_eu):
            flash("Invalid box price in EU", "danger")
            return redirect("/editBox")


        # Ensure the box express price was submitted
        if not price_ex:
            flash("must provide box express price", "warning")
            return redirect("/editBox")


        # Ensure the box express price fits server-side
        if not re.search("^[0-9]+\.?[0-9]+$", price_ex):
            flash("Invalid box express price", "danger")
            return redirect("/editBox")


        # Update box name, length, width, height, price DE, price EU and price EX into the table and commit
        query = Boxes.query.filter_by(id=box_id).first()
        query.name = name
        query.length = length
        query.width = width
        query.height = height
        query.price_de = price_de
        query.price_eu = price_eu
        query.price_ex = price_ex
        db.session.commit()


        # Flash result & redirect
        flash("Box edited", "success")
        return redirect("/administration")


    else:

        # Get arguments from url_for in administration
        thisBox = request.args.getlist("boxes")
        
    
        return render_template("editBox.html", name=getUserName(), picture=getUserPicture(), role=getUserRole(), boxes=thisBox)