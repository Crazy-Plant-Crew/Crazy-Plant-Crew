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


    # Get variable
    cost = 0
    boxesNE = []
    boxesEX = []
    boxes = []
    plantItems = []
    x = 0
    y = 0
    rotation = False
    checkerHorizonal = False
    checkerVertical = False


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
        boxesNE = sorted(boxesNE, key=lambda x: (int(x[1][4]), int(x[1][5]), int(x[1][6])), reverse=True)
        boxesEX = sorted(boxesEX, key=lambda x: (int(x[1][4]), int(x[1][5]), int(x[1][6])), reverse=True)


        # Make array with all the plants side-by-side and sort them 
        for plant in plants:
            index = int(plant[2])
            while index > 0:
                plantItems.extend([plant])
                index -= 1

        plantItems = sorted(plantItems, key=lambda x: (int(x[4]), int(x[5]), int(x[6])), reverse=True)


        # Function to take the biggest box needed from the express group first, then from the non express group.
        def plantLoop():
            """
            # Empty the boxes array
            boxes = []

            # Check weight
            """

            # Loop through plants
            for plantItem in plantItems:

                # Express only can only be in Germany - Append needed box
                if len(boxesEX) > 0 and len(plantItems) > 0 and addresses[3] == "Germany":
                    for boxEX in boxesEX:
                        if int(plantItem[0]) == int(boxEX[1][0]):
                            boxes.extend([boxEX[0]])
                            return

                # Non express but in Germany - Append needed box
                elif len(boxesNE) > 0 and len(plantItems) > 0 and addresses[3] == "Germany":
                    for boxNE in boxesNE:
                        if int(plantItem[0]) == int(boxNE[1][0]):
                            boxes.extend([boxNE[0]])
                            return
                
                # Non express in the EU - Append needed box
                elif len(boxesNE) > 0 and len(plantItems) > 0 and addresses[3] != "Germany":
                    for boxNE in boxesNE:
                        if int(plantItem[0]) == int(boxNE[1][0]):
                            boxes.extend([boxNE[0]])
                            return

                # Return False if there are no more plant to cover
                else:
                    return False

        plantLoop()


        # Make a grid from the last needed box to represent its bottom
        thisBox = [["0" for row in range(int(boxes[-1][1]))] for row in range(int(boxes[-1][2]))]


        # Filler function
        def drawLoop(x, y, length, width, rotation):

            print(x)
            print(y)
            print(length)
            print(width)
            print(rotation)

            # Fill up horizontally
            def drawHorizon(row):
                drawIndexH = 0
                while drawIndexH < len(row):

                    if rotation == False and drawIndexH >= x and drawIndexH < x + length:
                        row[drawIndexH] = "1"
                        drawIndexH += 1

                    elif rotation == True and drawIndexH >= x and drawIndexH < x + width:
                        row[drawIndexH] = "1"
                        drawIndexH += 1

                    else:
                        drawIndexH += 1

            # Fill up vertically
            drawIndexV = 0
            while drawIndexV < len(thisBox):

                if rotation == False and drawIndexV >= y and drawIndexV < y + width:
                    drawHorizon(thisBox[drawIndexV])
                    drawIndexV += 1

                elif rotation == True and drawIndexV >= y and drawIndexV < y + length:
                    drawHorizon(thisBox[drawIndexV])
                    drawIndexV += 1

                else:
                    drawIndexV += 1


        # Grid looper
        def gridLoop(length, width):

            # Horizontal checker for free space
            def gridHorizon(length, width, x, y, rotation, checkerHorizonal, checkerVertical, row):
                gridIndexH = 0
                while gridIndexH < len(row):
                    if row[gridIndexH] == "0":
                        if gridIndexH + length < len(row):
                            checkerHorizonal = True
                            x = gridIndexH
                            print("X equals: " + str(x))
                            return True

                        elif gridIndexH + width < len(row):
                            x = gridIndexH
                            return "Rotation"

                        else:
                            return False

                    else:
                        gridIndexH += 1


            # Vertical checker for free space
            gridIndexV = 0
            while gridIndexV < len(thisBox):
                if gridHorizon(length, width, x, y, rotation, checkerHorizonal, checkerVertical, thisBox[index]) == True:
                    if gridIndexV + y == width:
                        checkerVertical = True
                        return drawLoop(x, y, length, width, rotation)
                    
                    else:
                        gridIndexV += 1

                elif gridHorizon(length, width, x, y, rotation, checkerHorizonal, checkerVertical, thisBox[index]) == "Rotation":
                    if gridIndexV + y == length:
                        checkerVertical = True
                        checkerHorizonal = True
                        rotation = True
                        return drawLoop(x, y, length, width, rotation)

                    else:
                        gridIndexV += 1

                else:
                    y = gridIndexV
                    gridIndexV += 1


        gridLoop(70, 50)
        gridLoop(30, 10)


        """
        # Fill up first plant in that box bottom
        while len(plantItems) > 0:
            for plantItem in plantItems:
                length = int(plantItem[4])
                width = int(plantItem[5])
                gridLoop(length, width)
            
            del plantItems[0]


        # Delete basket items


        # Make the order valid
        print("ADDRESSES")
        print(addresses)
        print(len(addresses))
        print("PLANTS")
        print(plants)
        print(len(plants))
        print("NON EXPRESS")
        print(boxesNE)
        print(len(boxesNE))
        print("EXPRESS")
        print(boxesEX)
        print(len(boxesEX))
        print("PLANTITEMS")
        print(plantItems)
        print(len(plantItems))
        print("BOXES")
        print(boxes)
        print(len(boxes))
        print("COST")
        print(cost)
        """

        # Counter of 1's to check if results make sense
        def gridCounter():
            total0 = 0
            total1 = 0
            for row in thisBox:
                for unit in row:
                    if unit == "1":
                        total1 += 1
                    else:
                        total0 += 1

            return print("TOTAL ZERO IS: " + str(total0) + "// TOTAL ONE IS: " + str(total1))

        gridCounter()
    
        return render_template("confirmation.html", name=getUserName(), picture=getUserPicture(), role=getUserRole())