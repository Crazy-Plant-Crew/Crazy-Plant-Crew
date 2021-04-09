import traceback
import sys

from flask import Blueprint, render_template, redirect, session, request, flash, get_flashed_messages
from application import getUserName, getUserPicture, login_required, confirmed_required, getUserRole, role_required, db, Orders
from flask_sqlalchemy import SQLAlchemy


# Set Blueprints
transaction = Blueprint('transaction', __name__,)


@transaction.route("/transaction", methods=["GET", "POST"])
@login_required
@confirmed_required
def transactionFunction():    

    # Force flash() to get the messages on the same page as the redirect.
    get_flashed_messages()


    # Get variable
    user_id = session["user_id"]


    # Query database for orders
    orders = Orders.query.all()   


    # Make array of arrays of plants in Orders
    plants = []
    for order in orders:
        plants.extend([eval(order.plants)])


    # Make array of arrays of addresses in Orders
    addresses = []
    for order in orders:
        addresses.extend([eval(order.addresses)])


    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        print("Transaction")



    
    return render_template("transaction.html", name=getUserName(), picture=getUserPicture(), role=getUserRole(), zip=zip(orders, plants, addresses))