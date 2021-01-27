import traceback
import sys

from flask import Blueprint, render_template, redirect, session, request, flash, get_flashed_messages
from application import getUserName, getUserPicture, getUserRole, login_required, confirmed_required, db
from flask_sqlalchemy import SQLAlchemy

# Set Blueprints
index = Blueprint('index', __name__,)

@index.route("/", methods=["GET", "POST"])
@login_required
@confirmed_required
def indexFunction():

    # Force flash() to get the messages on the same page as the redirect.
    get_flashed_messages()


    if request.method == "POST":

        # Get variables
        plant_id = request.form.get("plant_id")
        user_id = session["user_id"]
        quantity = request.form.get("quantity")


        # Query database for plants name, picture, price
        record = db.engine.execute("SELECT * FROM Plants WHERE id=:id;", {"id": plant_id})
        plants = record.fetchall()
        name = plants[0][1]
        picture = plants[0][4]
        price = plants[0][3]
       

        # Get current plant stock
        record = db.engine.execute("SELECT stock FROM Plants WHERE id=:id;", {"id": plant_id})
        existingStock = record.fetchall()


        # Avoid going to negative stocks
        if len(existingStock) != 0:
            if int(existingStock[0][0]) - int(quantity) < 0:

                flash("Not enough in stock")
                return redirect("/")

        
        # Check for existing stock in the basket
        record = db.engine.execute("SELECT quantity FROM Baskets WHERE plant_id=:plant_id AND user_id=:user_id;", {"plant_id": plant_id, "user_id": user_id})
        existingQuantity = record.fetchall()


        # If there is already some plant in the basket
        if len(existingQuantity) > 0:


            # Sum the quantities
            newQuantity = int(existingQuantity[0][0]) + int(quantity)

            user_id = session["user_id"]
            subtotal = int(newQuantity) * int(price)
            
            # Update database with quantity
            db.engine.execute("UPDATE Baskets SET quantity=:quantity, subtotal=:subtotal WHERE plant_id=:plant_id AND user_id=:user_id", {"plant_id": plant_id, "user_id": user_id, "quantity": newQuantity, "subtotal": int(subtotal)})


        # First time the user has put this plant in the basket
        else:

            user_id = session["user_id"]
            subtotal = int(quantity) * int(price)
            
            # Update database with quantity
            db.engine.execute("INSERT INTO Baskets(plant_id, user_id, quantity, name, picture, price, subtotal) VALUES (:plant_id, :user_id, :quantity, :name, :picture, :price, :subtotal)", {"plant_id": plant_id, "user_id": user_id, "quantity": quantity, "name": name, "picture": picture, "price": price, "subtotal": int(subtotal)})


        flash("Added to basket")
        return redirect("/")


    else:

        # Query database for plants to display them
        show = "Yes"

        plants = Plants.query.filter_by(show=show).all()
        print(plants)

        return render_template("index.html", name=getUserName(), picture=getUserPicture(), role=getUserRole(), plants=plants)