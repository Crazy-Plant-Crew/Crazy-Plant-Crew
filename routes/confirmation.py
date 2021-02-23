import traceback
import sys

from flask import Blueprint, render_template, redirect, session, request, flash, get_flashed_messages
from application import getUserName, getUserPicture, login_required, confirmed_required, getUserRole, role_required, db, Orders, Boxes
from flask_sqlalchemy import SQLAlchemy
from time import time


# Set Blueprints
confirmation = Blueprint('confirmation', __name__,)


@confirmation.route("/confirmation", methods=["GET", "POST"])
@login_required
@confirmed_required
def confirmationFunction():    

    # Force flash() to get the messages on the same page as the redirect.
    get_flashed_messages()


    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Get variable
        date = int(time())
        packages = Boxes.query.all()

           
        # Fake pay varibale
        pay = request.form.get("pay")


        # Convert pay value to string
        if pay == None:
            pay = "No"
        if pay == "pay":
            pay = "Yes"


        # Insert pay and date into the table
        db.session.add(Orders(pay=pay, date=date))
        db.session.commit()


        # Flash result & redirect
        flash("Plant(s) ordered", "success")
        return redirect("/history")

    
    else:

        # Make boxes array from packages
        boxes = []
        for element in packages:
            print(element)
    
        return render_template("confirmation.html", name=getUserName(), picture=getUserPicture(), role=getUserRole())