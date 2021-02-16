import traceback
import sys

from flask import Blueprint, render_template, redirect, session, request
from application import getUserName, getUserPicture, login_required, confirmed_required, getUserRole, role_required, db, Boxes
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
        price_de = request.form.get("length")
        price_eu = request.form.get("width")
        price_ex = request.form.get("height")


        # Check length
        getInputLength(name, 100, "Name is too long (100)", "danger", "/addBox")
        getInputLength(length, 6, "Length is too big (6)", "danger", "/addBox")
        getInputLength(width, 6, "Price is too big (6)", "danger", "/addBox")
        getInputLength(height, 6, "Offer is too big (6)", "danger", "/addBox")
        getInputLength(price_de, 6, "Length is too big (6)", "danger", "/addBox")
        getInputLength(price_eu, 6, "Width is too big (6)", "danger", "/addBox")
        getInputLength(price_ex, 6, "Height is too big (6)", "danger", "/addBox")


        # Ensure the box name was submitted
        if not name:
            flash("must provide box name", "warning")
            return redirect("/addBox")


        # Ensure the box name fits server-side
        if not re.search("^[a-zA-Z 0-9]{1,100}$", name):
            flash("Invalid plant name", "danger")
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


        # Ensure the box price in DE was submitted
        if not price_de:
            flash("must provide box price in DE", "warning")
            return redirect("/addBox")


        # Ensure the box price in DE fits server-side
        if not re.search("^[0-9]+$", price_de):
            flash("Invalid box price in DE", "danger")
            return redirect("/addBox")


        # Ensure the box price in EU was submitted
        if not price_eu:
            flash("must provide box price in EU", "warning")
            return redirect("/addBox")


        # Ensure the box price in EU fits server-side
        if not re.search("^[0-9]+$", price_eu):
            flash("Invalid box price in EU", "danger")
            return redirect("/addBox")


        # Ensure the box express price was submitted
        if not price_ex:
            flash("must provide box express price", "warning")
            return redirect("/addBox")


        # Ensure the box express price fits server-side
        if not re.search("^[0-9]+$", price_ex):
            flash("Invalid box express price", "danger")
            return redirect("/addBox")


        # Insert box name, length, width, height, price DE, price EU and price EX into the table
        db.session.add(Plants(name=name, length=length, width=width, height=height, price_de=price_de, price_eu=price_eu, price_ex=price_ex))
        db.session.commit()


        # Flash result & redirect
        flash("Box added", "success")
        return redirect("/administration")


    else:
    
        return render_template("addBox.html", name=getUserName(), picture=getUserPicture(), role=getUserRole())