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

            # Check cost
            """

            # Loop through plants
            for plantItem in plantItems:

                # Express only can only be in Germany - Append needed box
                if len(boxesEX) > 0 and len(plantItems) > 0 and addresses[3] == "Germany":
                    for boxEX in boxesEX:
                        if int(plantItem[0]) == int(boxEX[1][0]):
                            return boxes.extend([boxEX[0]])

                # Non express but in Germany - Append needed box
                elif len(boxesNE) > 0 and len(plantItems) > 0 and addresses[3] == "Germany":
                    for boxNE in boxesNE:
                        if int(plantItem[0]) == int(boxNE[1][0]):
                            return boxes.extend([boxNE[0]])                            
                
                # Non express in the EU - Append needed box
                elif len(boxesNE) > 0 and len(plantItems) > 0 and addresses[3] != "Germany":
                    for boxNE in boxesNE:
                        if int(plantItem[0]) == int(boxNE[1][0]):
                            return boxes.extend([boxNE[0]])            

                # Return False if there are no more plant to cover
                else:
                    return False


        # Make a grid from the last needed box to represent its bottom
        def makeGrid():
            if len(boxes) > 0:
                thisBox = [["0" for row in range(int(boxes[-1][1]))] for row in range(int(boxes[-1][2]))]
                return thisBox

            else:
                return False


        # Take plants length and width
        def sizeLoop(index):
            if len(plantItems) > 0:
                length = plantItems[index][4]
                width = plantItems[index][5]
                return length, width

            else:
                return False


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

                elif rotation == True and drawIndexH >= x and drawIndexH < x + width:
                    row[drawIndexH] = "1"
                    drawIndexH += 1

                else:
                    drawIndexH += 1


        # Grid looper
        def gridLoop(length, width, thisBox):

            # Horizontal checker for free space
            def gridHorizon(row):
                gridIndexH = 0
                while gridIndexH < len(row):
                    if row[gridIndexH] == "0":
                        return gridIndexH

                    else:
                        gridIndexH += 1


            # Vertical checker for free space
            gridIndexV = 0
            while gridIndexV < len(thisBox):
                x = gridHorizon(thisBox[gridIndexV])
                if x <= int(len(thisBox[gridIndexV]) - int(length)):
                    rotation = False
                    if gridIndexV + width < len(thisBox):
                        if thisBox[gridIndexV + width][x] == "0":
                            y = gridIndexV
                            return drawLoop(x, y, length, width, rotation)

                        else:
                            gridIndexV += 1
                    else:
                        return False

                elif x <= int(len(thisBox[gridIndexV]) - int(width)):
                    rotation = True
                    if gridIndexV + length < len(thisBox):
                        if thisBox[gridIndexV + length][x] == "0":
                            y = gridIndexV
                            return drawLoop(x, y, length, width, rotation)
                        
                        else:
                            gridIndexV += 1

                    else:
                        return False

                else:
                    gridIndexV += 1


        def deleteLoop(index):
            if len(plantItems) > 0:
                del plantItems[index]
                return

            else:
                return False


        # Main loop for the sending costs
        def mainLoop():

            def fillBox():
                index = 0
                while index < len(plantItems):
                    if sizeLoop(index) != False:
                        length, width = sizeLoop(index)
                        if gridLoop(length, width, thisBox) == True:
                            if deleteLoop(index) != False:
                                index = 0
                                fillBox()
                            else:
                                return False
                        else:
                            index += 1
                    else:
                        return False


            if plantLoop() != False:
                if makeGrid() != False:
                    thisBox = makeGrid()
                    if sizeLoop(0) != False:
                        length, width = sizeLoop(0)
                        if gridLoop(length, width, thisBox) != False:                           
                            if deleteLoop(0) != False:
                                if fillBox() == False:
                                    mainLoop()

                                else:
                                    return
                            else:
                                return
                        else:
                            return
                    else:
                        return
                else:
                    return
            else:
                return                    
                




        # Make the order valid
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
        """

        mainLoop()
    
        return render_template("confirmation.html", name=getUserName(), picture=getUserPicture(), role=getUserRole())