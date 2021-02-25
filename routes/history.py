import traceback
import sys

from flask import Blueprint, render_template, redirect, session, request, flash, get_flashed_messages
from application import getUserName, getUserPicture, login_required, confirmed_required, getUserRole, role_required, db, Orders
from flask_sqlalchemy import SQLAlchemy


# Set Blueprints
history = Blueprint('history', __name__,)


@history.route("/history", methods=["GET", "POST"])
@login_required
@confirmed_required
def historyFunction():    

    # Force flash() to get the messages on the same page as the redirect.
    get_flashed_messages()


    # Get variable
    user_id = session["user_id"]


    # Query database for orders
    orders = Orders.query.filter_by(user_id=user_id).all()   


    # Make array of plants in Orders
    plants = []
    for order in orders:
        plants.extend(eval(order.plants))

    print(plants)
  

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        print("History")



    else:
    
        return render_template("history.html", name=getUserName(), picture=getUserPicture(), role=getUserRole(), zip=zip(orders, plants))