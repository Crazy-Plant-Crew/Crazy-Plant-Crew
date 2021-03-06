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
    query = Baskets.query.filter_by(user_id=user_id)


    # Make plants array from basket
    plants = []
    for element in query:
        plants.append([str(element.plant_id), str(element.name), str(element.quantity), str(element.price)])


    # Add to plants array the plants features
    index = 0
    while index < len(plants):
        query = Plants.query.filter_by(id=plants[index][0])
        for element in query:
            plants[index].extend([str(element.length), str(element.width), str(element.height), str(element.weight), str(element.express)])            
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

        boxesNE = []
        boxesEX = []
        boxes = []

        plantItems = []


        # Checking plants sizes and weight against boxes sizes and capacity, if it fits, append adapted box to array of possible needed box
        for plant in plants:
            for package in packaging:

                # Express only works in Germany
                if addresses[3] == "Germany":

                    # Check if express is needed for the whole
                    if express == "No":

                        # Check if express is needed on one plant
                        if plant[8] == "No":
                            if int(plant[4]) < int(package[1]) and int(plant[5]) < int(package[2]) and int(plant[6]) < int(package[3]) and int(plant[7]) < int(package[4]):
                                boxesNE.append([package, plant])
                                break
                            
                        # Check if express is needed on one plant
                        if plant[8] == "Yes":
                            if int(plant[4]) < int(package[1]) and int(plant[5]) < int(package[2]) and int(plant[6]) < int(package[3]) and int(plant[7]) < int(package[5]):
                                boxesEX.append([package, plant])
                                break

                    # Check if express is needed for the whole
                    if express == "Yes":

                        if int(plant[4]) < int(package[1]) and int(plant[5]) < int(package[2]) and int(plant[6]) < int(package[3]) and int(plant[7]) < int(package[5]):
                            boxesEX.append([package, plant])
                            break

                # Express only works in Germany
                if addresses[3] != "Germany":

                    if int(plant[4]) < int(package[1]) and int(plant[5]) < int(package[2]) and int(plant[6]) < int(package[3]) and int(plant[7]) < int(package[4]):
                        boxesNE.append([package, plant])
                        break

        """
        # Check if both arrays are not empty, if yes, send warning to user to contact Glenn
        """

        # Sort arrays boxes NE & RE
        boxesNE = sorted(boxesNE, key=lambda x: (x[1][4], x[1][5], x[1][6]))
        boxesEX = sorted(boxesEX, key=lambda x: (x[1][4], x[1][5], x[1][6]))


        # Make array with all the plants side-by-side and sort them 
        for plant in plants:
            index = int(plant[2])
            while index > 0:
                plantItems.extend([plant])
                index -= 1

        plantItems = sorted(plantItems, key=lambda x: (x[4], x[5], x[6]), reverse=True)


        # Sort the boxes per size


        # Make a grid from the smallest plants length & width and use the biggest plant height as ceiling for this level

        

        # Delete basket items


        # Make the order valid

        print("PLANTS")
        print(plants)
        print(len(plants))
        print("NON EXPRESS")
        print(boxesNE)
        print(len(boxesNE))
        print("EXPRESS")
        print(boxesEX)
        print(len(boxesEX))
        print("PLANTITEM")
        print(plantItems)
        print(len(plantItems))


    
        return render_template("confirmation.html", name=getUserName(), picture=getUserPicture(), role=getUserRole())