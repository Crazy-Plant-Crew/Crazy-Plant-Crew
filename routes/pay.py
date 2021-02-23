import traceback
import sys
import re

from flask import Blueprint, render_template, redirect, session, request, flash, get_flashed_messages
from application import getUserName, getUserPicture, login_required, confirmed_required, getUserRole, role_required, db, Boxes, Plants, Baskets, Orders, getInputLength
from flask_sqlalchemy import SQLAlchemy


# Set Blueprints
pay = Blueprint('pay', __name__,)


@pay.route("/pay", methods=["GET", "POST"])
@login_required
@confirmed_required
def payFunction():    

    # Force flash() to get the messages on the same page as the redirect.
    get_flashed_messages()


    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Get variable
        street = request.form.get("street")
        house = request.form.get("house")
        zipcode = request.form.get("zipcode")
        country = request.form.get("country")
        express = request.form.get("express")
        additional = request.form.get("additional")
        user_id = session["user_id"]
        selection = Baskets.query.filter_by(user_id=user_id)


        # Check length
        getInputLength(street, 100, "Street name is too long (100)", "danger", "/pay")
        getInputLength(house, 10, "House number is too big (10)", "danger", "/pay")
        getInputLength(zipcode, 10, "Zip code is too big (10)", "danger", "/pay")
        getInputLength(country, 100, "Country name is too long (100)", "danger", "/pay")
        getInputLength(additional, 800, "Additional information is too long (800)", "danger", "/pay")


        # Make plants array from selection
        plants = []
        for element in selection:

            plants.append([str(element.id), str(element.name), str(element.quantity), str(element.price)])
 

        # Add to plants array the plants features
        index = 0
        while index < len(plants):

            print("ID HERE")
            print(int(plants[index][0]))

            query = Plants.query.filter_by(id=int(plants[index][0])).first()

            print("QUERY HERE")
            print(query)
            print(query.length)

            """
            for element in query:

                plants[index].append(str(query.length), str(query.width), str(query.height), str(query.weight), str(query.express))
            """
            
            index += 1


        # Convert pay value to string
        if express == None:
            express = "No"
        if express == "express":
            express = "Yes"


        # Ensure the street name was submitted
        if not street:
            flash("must provide box name", "warning")
            return redirect("/pay")


        # Ensure the street name fits server-side
        if not re.search("^[a-zA-Z 0-9]{1,100}$", street):
            flash("Invalid street name", "danger")
            return redirect("/pay")


        # Ensure the house number was submitted
        if not house:
            flash("must provide a house number", "warning")
            return redirect("/pay")


        # Ensure the house number fits server-side
        if not re.search("^[a-zA-Z 0-9]{1,10}$", house):
            flash("Invalid house number", "danger")
            return redirect("/pay")


        # Ensure the zip code was submitted
        if not zipcode:
            flash("must provide a zip code", "warning")
            return redirect("/pay")


        # Ensure the zip code fits server-side
        if not re.search("^[a-zA-Z 0-9]{1,10}$", zipcode):
            flash("Invalid a zip code", "danger")
            return redirect("/pay")


        # Ensure the country was submitted
        if country == "None":
            flash("must provide a country", "warning")
            return redirect("/pay")


        # Ensure the country fits server-side
        if not re.search("^[a-zA-Z 0-9]{1,100}$", country):
            flash("Invalid a country", "danger")
            return redirect("/pay")


        # Insert street name, house number, zipcode, country, additional information, pay and user_id into the table
        db.session.add(Orders(street=street, house=house, zipcode=zipcode, country=country, express=express, additional=additional, user_id=user_id, plants=plants))
        db.session.commit()


        # Flash result & redirect
        flash("Parcel informations saved", "success")
        return redirect("/confirmation")

        

    else:

        countries = ["Austria", "Belgium", "Bulgaria", "Croatia", "Cyprus", "Czechia", "Denmark", "Estonia", "Finland", "France", "Germany", "Greece", "Hungary", "Ireland", "Italy", "Latvia", "Lithuania", "Luxembourg", "Malta", "Netherlands", "Poland", "Portugal", "Romania", "Slovakia", "Slovenia", "Spain", "Sweden"]

    
        return render_template("pay.html", name=getUserName(), picture=getUserPicture(), role=getUserRole(), countries=countries)