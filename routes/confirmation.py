import traceback
import sys

from flask import Blueprint, render_template, redirect, session, request, flash, get_flashed_messages, url_for
from application import getUserName, getUserPicture, login_required, confirmed_required, getUserRole, role_required, db, Orders, Boxes, Users, Plants, Baskets
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


    # Get variable
    user_id = session["user_id"]
    selection = Baskets.query.filter_by(user_id=user_id)


    # Make plants array from selection
    plants = []
    for element in selection:
        plants.append([str(element.id), str(element.name), str(element.quantity), str(element.price)])


    # Add to plants array the plants features
    index = 0
    while index < len(plants):
        query = Plants.query.filter_by(id=int(plants[index][0])).first()
        plants[index].extend([str(query.length), str(query.width), str(query.height), str(query.weight), str(query.express)])            
        index += 1


    # Make address array
    addresses = []
    query = Users.query.filter_by(id=user_id).first()
    addresses.extend([query.street, query.house, query.zipcode, query.country, query.additional])


    # Make express variable
    express = query.express


    # Make array with available boxes
    query = Boxes.query.all()
    packaging = []
    for element in query:
        packaging.append([str(element.name), str(element.length), str(element.width), str(element.height), str(element.weight_ne), str(element.weight_ex), str(element.price_de), str(element.price_eu), str(element.price_ex)])


    # Make array with needed boxes
    boxes = []


    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Get variable
        date = int(time())
        user_id = session["user_id"]
        
           
        # Fake pay varibale
        pay = request.form.get("pay")


        # Convert pay value to string
        if pay == None:
            pay = "No"
        if pay == "pay":
            pay = "Yes"


        if pay == "Yes":

            # Insert order informations into the orders table
            db.session.add(Orders(user_id=user_id, pay=pay, date=date, express=express, plants=str(plants), addresses=str(addresses), boxes=str(boxes)))
            db.session.commit()

            # Flash result & redirect
            flash("Plant(s) ordered", "success")
            return redirect("/history")


        if pay != "Yes":

            # Flash result & redirect
            flash("Payment not completed ", "warning")
            return redirect("/confirmation")


    
    else:

        # Get variable
        cost = 0
 

        # Checking plants sizes against boxes sizes, if it fits, append adapted box to array
        inner = 0
        outer = 0
        while outer < len(plants):
            while inner < len(packaging):
                if int(plants[outer][4]) < int(packaging[inner][1]) and int(plants[outer][5]) < int(packaging[inner][2]) and int(plants[outer][6]) < int(packaging[inner][3]):
                    boxes.append(packaging[inner])
                    inner = 0
                    outer += 1

            inner += 1

        print(boxes)


                
                
                

        """
        print("PLANTS")
        print(plants)
        print("ADDRESSES")
        print(addresses)
        print("EXPRESS")
        print(express)
        print("PACKAGING")
        print(packaging)
        print("BOXES")
        print(boxes)
        """

    
        return render_template("confirmation.html", name=getUserName(), picture=getUserPicture(), role=getUserRole())