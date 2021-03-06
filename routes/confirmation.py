import traceback
import sys
import os

from flask import Blueprint, render_template, redirect, session, request, flash, get_flashed_messages, url_for
from application import getUserName, getUserPicture, login_required, confirmed_required, getUserRole, role_required, sendMail, db, Orders, Boxes, Users, Plants, Baskets
from flask_sqlalchemy import SQLAlchemy
from time import time, ctime

# Set Blueprints
confirmation = Blueprint('confirmation', __name__,)


@confirmation.route("/confirmation", methods=["GET", "POST"])
@login_required
@confirmed_required
def confirmationFunction():    

    # Force flash() to get the messages on the same page as the redirect.
    get_flashed_messages()


    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Fake pay varibale
        pay = request.form.get("pay")


        # Get variable
        user_id = session["user_id"]
        date = ctime(time())
        plants = []
        items = []
        addresses = []
        total = 0


        # Convert pay value to string
        if pay == None:
            pay = "No"
        if pay == "pay":
            pay = "Yes"


        if pay == "Yes":

            # Update pay variable
            query = Orders.query.filter_by(user_id=user_id).all()
            query[-1].pay = "Yes"
            total = query[-1].total
            db.session.commit()


            # Make plants array from basket
            query = Baskets.query.filter_by(user_id=user_id)
            for element in query:
                plants.append([str(element.plant_id), str(element.name), str(element.quantity), str(element.price)])


            # Add to plants array the plants features
            index = 0
            while index < len(plants):
                query = Plants.query.filter_by(id=plants[index][0])
                for element in query:
                    plants[index].extend([str(element.length), str(element.width), str(element.height), str(element.weight), str(element.express)])            
                index += 1


            # Make array with all the plants side-by-side and sort them 
            for plant in plants:
                index = int(plant[2])
                while index > 0:
                    items.extend([plant])
                    index -= 1


            # Make address array
            query = Users.query.filter_by(id=user_id).first()
            addresses.extend([query.first, query.last, query.caresof, query.street, query.house, query.zipcode, query.city, query.country, query.additional])


            # Delete basket in DB
            Baskets.query.filter_by(user_id=user_id).delete()
            db.session.commit()


            # Update stock in Plants
            for item in items:

                # Query for plant stock of corresponding id
                query = Plants.query.filter_by(id=item[0]).first()

                # Check if there is still at least one unit
                if query.stock >= 1:

                    # decrement by one & commit
                    query.stock -= 1
                    db.session.commit()

                else:

                    # Flash result & redirect
                    flash("Not enough stock of " + str(itemCopy[1]), "danger")
                    return redirect("/basket")



            # Send order confirmation email to client 
            subject = "Your order from the Crazy Plant Crew"
            query = Users.query.filter_by(id=user_id).first()
            email = query.email
            body = render_template('order.html', name=getUserName(), addresses=addresses, plants=plants, total=total, date=date)
            sendMail(subject, email, body)


            # Send closed deal email to Glenn 
            subject = "You closed a deal!"
            email = os.environ["EMAIL_SEND"]
            body = render_template('deal.html', name=getUserName(), addresses=addresses, total=total, date=date)
            sendMail(subject, email, body)


            # Flash result & redirect
            flash("Plant(s) ordered", "success")
            return redirect("/history")


        if pay != "Yes":

            # Flash result & redirect
            flash("Payment not completed ", "warning")
            return redirect("/confirmation")


    
    else:

        # Get variable
        user_id = session["user_id"]
        date = ctime(time())
        pay = "No"
        subtotal = 0
        shipping = 0
        total = 0
        cost = []
        addresses = []
        plants = []
        items = []
        boxesNE = []
        boxesEX = []
        boxes = []
        packaging = []
        weight = []


        # Make plants array from basket
        query = Baskets.query.filter_by(user_id=user_id)
        for element in query:
            plants.append([str(element.plant_id), str(element.name), str(element.quantity), str(element.price)])
            subtotal += element.subtotal


        # Add to plants array the plants features
        index = 0
        while index < len(plants):
            query = Plants.query.filter_by(id=plants[index][0])
            for element in query:
                plants[index].extend([str(element.length), str(element.width), str(element.height), str(element.weight), str(element.express)])            
            index += 1


        # Make address array
        query = Users.query.filter_by(id=user_id).first()
        addresses.extend([query.first, query.last, query.caresof, query.street, query.house, query.zipcode, query.city, query.country, query.additional])


        # Make express variable
        express = query.express


        # Make array with available boxes
        query = Boxes.query.all()
        for element in query:
            packaging.append([str(element.name), str(element.length), str(element.width), str(element.height), str(element.weight_ne), str(element.weight_ex), str(element.price_de), str(element.price_eu), str(element.price_ex)])


        # Check if boxes are in the system
        if len(packaging) == 0:
            
            # Flash result & redirect
            flash("There are no box available", "danger")
            return redirect("/basket")


        # Checking plants sizes and weight against boxes sizes and capacity, if it fits, append adapted box to array of possible needed box
        for plant in plants:
            for package in packaging:

                # Express only works in Germany
                if addresses[7] == "Germany":

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
                if addresses[7] != "Germany":

                    if int(plant[4]) < int(package[1]) and int(plant[5]) < int(package[2]) and int(plant[6]) < int(package[3]) and int(plant[7]) < int(package[4]):
                        boxesNE.append([package, plant])
                        break


        # Sort arrays boxes NE & RE
        boxesNE = sorted(boxesNE, key=lambda x: (int(x[1][4]), int(x[1][5]), int(x[1][6])), reverse=True)
        boxesEX = sorted(boxesEX, key=lambda x: (int(x[1][4]), int(x[1][5]), int(x[1][6])), reverse=True)


        # Make array with all the plants side-by-side and sort them 
        for plant in plants:
            index = int(plant[2])
            while index > 0:
                items.extend([plant])
                index -= 1

        items = sorted(items, key=lambda x: (int(x[4]), int(x[5]), int(x[6])), reverse=True)


        # Function to take the biggest box needed from the express group first, then from the non express group. Increment sending costs.
        def plantLoop(thisPlant):

            # Express only can only be in Germany - Append needed box - Append to cost
            if len(boxesEX) > 0 and express == "Yes" and addresses[7] == "Germany":
                for boxEX in boxesEX:
                    if int(thisPlant[0]) == int(boxEX[1][0]):
                        cost.append(float(boxEX[0][8]))
                        boxes.extend([boxEX[0]])
                        weight.append(int(boxEX[0][5]))
                        return

            # Express only can only be in Germany - Append needed box - Append to cost
            if len(boxesEX) > 0 and express == "No" and thisPlant[8] == "Yes" and addresses[7] == "Germany":
                for boxEX in boxesEX:
                    if int(thisPlant[0]) == int(boxEX[1][0]):
                        boxes.extend([boxEX[0]])
                        cost.append(float(boxEX[0][8]))
                        weight.append(int(boxEX[0][5]))
                        return

            # Non express but in Germany - Append needed box - Append to cost
            elif len(boxesNE) > 0 and express == "No" and thisPlant[8] == "No" and addresses[7] == "Germany":
                for boxNE in boxesNE:
                    if int(thisPlant[0]) == int(boxNE[1][0]):
                        boxes.extend([boxNE[0]])
                        cost.append(float(boxNE[0][6]))
                        weight.append(int(boxNE[0][4]))
                        return                      
            
            # Non express in the EU - Append needed box - Append to cost
            elif len(boxesNE) > 0 and express == "No" and addresses[7] != "Germany":
                for boxNE in boxesNE:
                    if int(thisPlant[0]) == int(boxNE[1][0]):
                        boxes.extend([boxNE[0]])
                        cost.append(float(boxNE[0][7]))
                        weight.append(int(boxNE[0][4]))
                        return     

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
        def getAttributes(thisPlant):
            if len(items) > 0:
                length = thisPlant[4]
                width = thisPlant[5]
                mass = thisPlant[7]
                return length, width, mass

            else:
                return False


        # Filler function
        def drawLoop(x, y, length, width, rotation, thisBox):

            # Fill up horizontally
            def drawHorizon(row):
                drawIndexH = 0
                while drawIndexH < len(row):

                    if rotation == False and drawIndexH >= x and drawIndexH < x + int(length):
                        row[drawIndexH] = "1"
                        drawIndexH += 1

                    elif rotation == True and drawIndexH >= x and drawIndexH < x + int(width):
                        row[drawIndexH] = "1"
                        drawIndexH += 1

                    else:
                        drawIndexH += 1

            # Fill up vertically
            drawIndexV = 0
            while drawIndexV < len(thisBox):

                if rotation == False and drawIndexV >= y and drawIndexV < y + int(width):
                    drawHorizon(thisBox[drawIndexV])
                    drawIndexV += 1

                elif rotation == True and drawIndexV >= x and drawIndexV < x + int(width):
                    drawHorizon(thisBox[drawIndexV])
                    drawIndexV += 1

                else:
                    drawIndexV += 1


        # Grid looper
        def gridLoop(length, width, thisBox):

            # Horizontal checker for free space
            def gridHorizon(row):
                gridIndexH = 0
                while gridIndexH < len(row):

                    # Search of a "0"
                    if row[gridIndexH] == "0":

                        # Return first available "0"
                        return gridIndexH

                    else:
                        gridIndexH += 1


            # Vertical checker for free space
            gridIndexV = 0
            while gridIndexV < len(thisBox):

                # Get free space horizontally
                x = gridHorizon(thisBox[gridIndexV])

                # X must exist otherwise the plant never fits
                if x != None:

                    # Check if fits with the length horizontally
                    if x <= int(len(thisBox[gridIndexV]) - int(length)):

                        # Check if fits with width vertically
                        if gridIndexV + int(width) < len(thisBox):

                            # Check if we find a "0" to be sure there is enough space
                            if thisBox[gridIndexV + int(width)][x] == "0":

                                # Set roation flag
                                rotation = False

                                # Set the y axis
                                y = gridIndexV

                                # Start drawing
                                return drawLoop(x, y, length, width, rotation, thisBox)

                            else:
                                gridIndexV += 1
                                
                        else:
                            return False

                    # Check if fits with width horizontally (flipped)
                    elif x <= int(len(thisBox[gridIndexV]) - int(width)):

                        # Check if fits with length vertically
                        if gridIndexV + int(length) < len(thisBox):

                            # Check if we find a "0" to be sure there is enough space
                            if thisBox[gridIndexV + int(length)][x] == "0":

                                # Set rotation flag
                                rotation = True

                                # Set the y axis
                                y = gridIndexV

                                # Start drawing
                                return drawLoop(x, y, length, width, rotation, thisBox)
                            
                            else:
                                gridIndexV += 1

                        else:
                            gridIndexV += 1

                    else:
                        gridIndexV += 1

                else:
                    return False


        # Delete dealt plants and update corresponding stock
        def deleteLoop(thisPlant):
            if len(items) > 0:

                return items.remove(thisPlant)

            else:
                return False


        # Master loop
        def masterLoop():

            # Check for other plants to fit present box
            def slaveLoop(thisBox):
                if len(items) > 0:
                    for item in items:

                        # Get needed attributes
                        length, width, mass = getAttributes(item)

                        # Check if there is enough available weight
                        if weight[-1] - int(mass) > 0:

                            # Update available weight
                            weight[-1] -= int(mass)

                            # Check if possible to draw an other plant in the grid
                            if gridLoop(length, width, thisBox) != False:      

                                # Delete dealt plant                      
                                deleteLoop(item)

                                # Recursively try again
                                slaveLoop(thisBox)

                            else:
                                masterLoop()
                                
                        else:
                            masterLoop()
                    
                else:
                    return

            # Start dealing with every plants
            if len(items) > 0:
                for item in items:

                    # Take needed box
                    plantLoop(item)

                    # Make a grid and get needed attributes
                    thisBox = makeGrid()
                    length, width, mass = getAttributes(item)

                    # Check if there is enough available weight
                    if weight[-1] - int(mass) > 0:

                        # Update available weight
                        weight[-1] -= int(mass)

                        # Fill up grid
                        gridLoop(length, width, thisBox)

                        # Delete dealt plants
                        deleteLoop(item)

                        # Start slaveLoop to check if other plants can fit in that box
                        slaveLoop(thisBox)

                    else:
                        return

            return


        # Start main loop
        masterLoop()


        # Get total shipping cost
        for element in cost:
            shipping += element

        total = shipping + subtotal


        # Insert order informations into the orders table
        db.session.add(Orders(user_id=user_id, date=date, plants=str(plants), boxes=str(boxes), addresses=str(addresses), express=express, pay=pay, shipping=shipping, subtotal=subtotal, total=total))
        db.session.commit()


    
        return render_template("confirmation.html", name=getUserName(), picture=getUserPicture(), role=getUserRole(), subtotal=subtotal, shipping=shipping, total=total)