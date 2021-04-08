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
    thisBasketItems = []
    

    # Query database for plants
    thisBasket = Baskets.query.filter_by(user_id=user_id).all()


    # Query database for plants
    baskets = Baskets.query.all()


    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Check if user deletes an item in the basket
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

            # Check if there are plants in the basket
            for item in thisBasket:
                thisBasketItems.append(item.name)


            if len(thisBasketItems) == 0:

                # Flash result & redirect
                flash("There are no plants to order", "danger")
                return redirect("/basket")


            # Set flag
            flag = False


            # Loop through the user basket
            for item in thisBasket:

                # Check with respective id's against Plants
                query = Plants.query.filter_by(id=item.plant_id).first()

                # If user orders too much 
                if item.quantity > query.stock:

                    # Set flag to True
                    flag = True


                    # Adapting basket to stock quantity and correct basket subtotal
                    item.quantity = query.stock
                    item.subtotal = int(query.stock) * float(item.price)
                    db.session.commit()


                    # Flash result & redirect
                    flash("Not enough stock of: " + str(item.name), "warning")
                    flash("Adapting, only " + str(query.stock) + " available", "warning")

                else:
                    flag = False


            # Check for flag status
            if flag == True:
                return redirect("/basket")

            else:
                return redirect("/pay")




    else:

        # Get total price
        total = 0
        for element in thisBasket:

            total += element.subtotal

    
        return render_template("basket.html", name=getUserName(), picture=getUserPicture(), role=getUserRole(), baskets=thisBasket, total=total)