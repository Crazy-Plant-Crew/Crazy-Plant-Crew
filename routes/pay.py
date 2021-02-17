import traceback
import sys
import re

from flask import Blueprint, render_template, redirect, session, request, flash, get_flashed_messages
from application import getUserName, getUserPicture, login_required, confirmed_required, getUserRole, role_required, db, Boxes, Users, Plants, Baskets
from flask_sqlalchemy import SQLAlchemy


# Set Blueprints
pay = Blueprint('pay', __name__,)


@pay.route("/pay", methods=["GET", "POST"])
@login_required
@confirmed_required
def payFunction():    

    # Force flash() to get the messages on the same page as the redirect.
    get_flashed_messages()


    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Get variable
        street = request.form.get("street")
        house = request.form.get("house")
        zipcode = request.form.get("zipcode")
        country = request.form.get("country")
        additional = request.form.get("additional")
        

    else:
    
        return render_template("pay.html", name=getUserName(), picture=getUserPicture(), role=getUserRole())