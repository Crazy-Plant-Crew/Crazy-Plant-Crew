import traceback
import sys

from flask import Blueprint, render_template, redirect, session, request, flash, get_flashed_messages
from application import getUserName, getUserPicture, login_required, confirmed_required, getUserRole, role_required, db, Baskets, Plants
from flask_sqlalchemy import SQLAlchemy


# Set Blueprints
basket = Blueprint('basket', __name__,)

@basket.route("/basket", methods=["GET", "POST"])
@login_required
@confirmed_required
def basketFunction():    

    # Force flash() to get the messages on the same page as the redirect.
    get_flashed_messages()


    # Get variable
    user_id = session["user_id"]
    

    # Query database for plants
    thisBasket = Baskets.query.filter_by(user_id=user_id)


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


        # Check for available quantities
        if "pay" in request.form:

            # Loop through the user basket
            for item in thisBasket:

                # Check with respective id's against Plants
                query = Plants.query.filter_by(plant_id=item.id).first()

                # If user orders too much 
                if item.quantity > query.stock:

                    # Flash result & redirect
                    flash("Not enough stock of: " + str(item.name), "warning")
                    return redirect("/basket")

                # If user does not order too much
                else:
                    return redirect("/pay")


    else:

        # Get total price
        total = 0
        for element in thisBasket:

            total += element.subtotal

    
        return render_template("basket.html", name=getUserName(), picture=getUserPicture(), role=getUserRole(), baskets=thisBasket, total=total)