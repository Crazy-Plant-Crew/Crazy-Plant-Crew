import traceback
import sys
import re

from flask import Blueprint, render_template, redirect, session, request, get_flashed_messages, flash
from application import getUserName, getUserPicture, login_required, confirmed_required, getUserRole, role_required, db, Boxes, getInputLength
from flask_sqlalchemy import SQLAlchemy


# Set Blueprints
addBox = Blueprint('addBox', __name__,)


@addBox.route("/addBox", methods=["GET", "POST"])
@login_required
@confirmed_required
@role_required
def addBoxFunction():    

    # Force flash() to get the messages on the same page as the redirect.
    get_flashed_messages()


    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Get variable
        name = request.form.get("name")
        length = request.form.get("length")
        width = request.form.get("width")
        height = request.form.get("height")
        weight_ne = request.form.get("weight_ne")
        weight_ex = request.form.get("weight_ex")
        price_de = request.form.get("price_de")
        price_eu = request.form.get("price_eu")
        price_ex = request.form.get("price_ex")


        # Check length
        getInputLength(name, 100, "Name is too long (100)", "danger", "/addBox")
        getInputLength(length, 6, "Length is too big (6)", "danger", "/addBox")
        getInputLength(width, 6, "Width is too big (6)", "danger", "/addBox")
        getInputLength(height, 6, "Height is too big (6)", "danger", "/addBox")
        getInputLength(weight_ne, 6, "Weight non-express is too big (6)", "danger", "/addBox")
        getInputLength(weight_ex, 6, "Weight express is too big (6)", "danger", "/addBox")
        getInputLength(price_de, 6, "Price for DE is too big (6)", "danger", "/addBox")
        getInputLength(price_eu, 6, "Price for EU is too big (6)", "danger", "/addBox")
        getInputLength(price_ex, 6, "Price for Express is too big (6)", "danger", "/addBox")


        # Ensure the box name was submitted
        if not name:
            flash("must provide box name", "warning")
            return redirect("/addBox")


        # Ensure the box name fits server-side
        if not re.search("^[a-zA-Z 0-9]{1,100}$", name):
            flash("Invalid box name", "danger")
            return redirect("/addBox")


        # Ensure the box length was submitted
        if not length:
            flash("must provide box length", "warning")
            return redirect("/addBox")


        # Ensure the box length fits server-side
        if not re.search("^[0-9]+$", length):
            flash("Invalid box length", "danger")
            return redirect("/addBox")


        # Ensure the box width was submitted
        if not width:
            flash("must provide box width", "warning")
            return redirect("/addBox")


        # Ensure the box width fits server-side
        if not re.search("^[0-9]+$", width):
            flash("Invalid box width", "danger")
            return redirect("/addBox")


        # Ensure the box height was submitted
        if not height:
            flash("must provide box height", "warning")
            return redirect("/addBox")


        # Ensure the box height fits server-side
        if not re.search("^[0-9]+$", height):
            flash("Invalid box height", "danger")
            return redirect("/addBox")


        # Ensure the box weight_ne was submitted
        if not weight_ne:
            flash("must provide box weight non-express", "warning")
            return redirect("/addBox")


        # Ensure the box weight_ne fits server-side
        if not re.search("^[0-9]+$", weight_ne):
            flash("Invalid box weight non-express", "danger")
            return redirect("/addBox")


        # Ensure the box weight_ex was submitted
        if not weight_ex:
            flash("must provide box weight express", "warning")
            return redirect("/addBox")


        # Ensure the box weight_ex fits server-side
        if not re.search("^[0-9]+$", weight_ex):
            flash("Invalid box weight express", "danger")
            return redirect("/addBox")


        # Ensure the box price in DE was submitted
        if not price_de:
            flash("must provide box price in DE", "warning")
            return redirect("/addBox")


        # Ensure the box price in DE fits server-side
        if not re.search("^[0-9]+\.?[0-9]+$", format(float(price_de), ".2f")):
            flash("Invalid box price in DE", "danger")
            return redirect("/addBox")


        # Ensure the box price in EU was submitted
        if not price_eu:
            flash("must provide box price in EU", "warning")
            return redirect("/addBox")


        # Ensure the box price in EU fits server-side
        if not re.search("^[0-9]+\.?[0-9]+$", format(float(price_eu), ".2f")):
            flash("Invalid box price in EU", "danger")
            return redirect("/addBox")


        # Ensure the box express price was submitted
        if not price_ex:
            flash("must provide box express price", "warning")
            return redirect("/addBox")


        # Ensure the box express price fits server-side
        if not re.search("^[0-9]+\.?[0-9]+$", format(float(price_ex), ".2f")):
            flash("Invalid box express price", "danger")
            return redirect("/addBox")


        # Insert box name, length, width, height, price DE, price EU and price EX into the table
        db.session.add(Boxes(name=name, length=length, width=width, height=height, weight_ne=weight_ne, weight_ex=weight_ex, price_de=price_de, price_eu=price_eu, price_ex=price_ex))
        db.session.commit()


        # Flash result & redirect
        flash("Box added", "success")
        return redirect("/administration")


    else:
    
        return render_template("addBox.html", name=getUserName(), picture=getUserPicture(), role=getUserRole())