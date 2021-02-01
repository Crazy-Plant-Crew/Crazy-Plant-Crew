import traceback
import sys

from flask import Blueprint, render_template, redirect, session, request, flash, get_flashed_messages
from application import getUserName, getUserPicture, login_required, confirmed_required, getUserRole, role_required, db, Baskets
from flask_sqlalchemy import SQLAlchemy


# Set Blueprints
basket = Blueprint('basket', __name__,)

@basket.route("/basket", methods=["GET", "POST"])
@login_required
@confirmed_required
def basketFunction():    

    # Force flash() to get the messages on the same page as the redirect.
    get_flashed_messages()


    # Query database for plants
    baskets = Baskets.query.all()


    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        if "delete" in request.form:
        
            # Loop through the record list to match plant ID when delete button is pressed
            index = 0
            while index < len(baskets):

                if int(request.form["delete"]) == int(baskets[index].id):

                    # Query database for plant id to delete row                        
                    Baskets.query.filter(Baskets.id == baskets[index].id).delete()
                    db.session.commit()


                    # Flash result & redirect
                    flash("Item deleted", "success")
                    return redirect("/basket")

                else:

                    index += 1


    else:

        # Get total price
        index = 0
        total = 0
        while index < len(baskets):

            total += baskets[index].subtotal
            index += 1
    
        return render_template("basket.html", name=getUserName(), picture=getUserPicture(), role=getUserRole(), baskets=baskets, total=int(total))