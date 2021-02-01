import traceback
import sys

from flask import Blueprint, render_template, redirect, session, request, flash, get_flashed_messages
from application import getUserName, getUserPicture, getUserRole, login_required, confirmed_required, db, Users, Baskets, Plants, News
from flask_sqlalchemy import SQLAlchemy


# Set Blueprints
index = Blueprint('index', __name__,)


@index.route("/", methods=["GET", "POST"])
@login_required
@confirmed_required
def indexFunction():

    # Force flash() to get the messages on the same page as the redirect.
    get_flashed_messages()


    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Get variable
        plant_id = request.form.get("plant_id")
        user_id = session["user_id"]
        quantity = request.form.get("quantity")


        # Query database for plants name, picture, price and stock
        query = Plants.query.filter_by(id=plant_id).first()
        name = query.name
        picture = query.picture
        price = query.price
        existingStock = query.stock


        # Avoid going to negative stocks
        if int(existingStock) - int(quantity) < 0:
                flash("Not enough in stock", "Warning")
                return redirect("/")

        
        # Check for existing stock in the basket
        query = Baskets.query.filter_by(plant_id=plant_id, user_id=user_id).first()
        if query != None:
            existingQuantity = query.quantity
        else:
            existingQuantity = 0


        # If there is already some plant in the basket
        if existingQuantity > 0:

            # Sum up the quantities
            newQuantity = existingQuantity + int(quantity)
            user_id = session["user_id"]
            subtotal = int(newQuantity) * int(price)
            
            # Update database with quantity
            query = Baskets.query.filter_by(plant_id=plant_id).filter_by(user_id=user_id).first()
            query.quantity = newQuantity
            query.subtotal = subtotal
            db.session.commit()


        # First time the user has put this plant in the basket
        else:

            user_id = session["user_id"]
            subtotal = int(quantity) * int(price)
            
            # Add quantity to database
            db.session.add(Baskets(plant_id=plant_id, user_id=user_id, quantity=quantity, name=name, picture=picture, price=price, subtotal=subtotal))
            db.session.commit()
            

        # Flash result & redirect
        flash("Added to basket", "Information")
        return redirect("/")


    else:

        # Query database for plants to display them
        show = "Yes"
        plants = Plants.query.filter_by(show=show).all()


        return render_template("index.html", name=getUserName(), picture=getUserPicture(), role=getUserRole(), plants=plants)