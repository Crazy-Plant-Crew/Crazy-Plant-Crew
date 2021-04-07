import traceback
import sys
import re

from flask import Blueprint, render_template, redirect, session, request, flash, get_flashed_messages, url_for
from application import getUserName, getUserPicture, login_required, confirmed_required, getUserRole, role_required, db, Boxes, Users, Plants, Baskets, Orders, getInputLength
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
        first = request.form.get("first")
        last = request.form.get("last")
        caresof = request.form.get("caresof")
        street = request.form.get("street")
        house = request.form.get("house")
        zipcode = request.form.get("zipcode")
        city = request.form.get("city")
        country = request.form.get("country")
        express = request.form.get("express")
        additional = request.form.get("additional")
        user_id = session["user_id"]
        

        # Check length
        getInputLength(first, 100, "First name is too long (100)", "danger", "/pay")
        getInputLength(last, 100, "Last name is too long (100)", "danger", "/pay")
        getInputLength(caresof, 100, "C/O name is too long (100)", "danger", "/pay")
        getInputLength(street, 100, "Street name is too long (100)", "danger", "/pay")
        getInputLength(house, 10, "House number is too big (10)", "danger", "/pay")
        getInputLength(zipcode, 10, "Zip code is too big (10)", "danger", "/pay")
        getInputLength(city, 100, "City name is too long (100)", "danger", "/pay")
        getInputLength(country, 100, "Country name is too long (100)", "danger", "/pay")
        getInputLength(additional, 800, "Additional information is too long (800)", "danger", "/pay")


        # Convert pay value to string
        if express == None:
            express = "No"
        if express == "express":
            express = "Yes"


        # Convert caresof value to string
        if caresof == None:
            caresof = "No C/O"


        # Ensure the first name was submitted
        if not first:
            flash("must provide first name", "warning")
            return redirect("/pay")


        # Ensure the first name fits server-side
        if not re.search("^[a-zA-Z 0-9]{1,100}$", first):
            flash("Invalid first name", "danger")
            return redirect("/pay")


        # Ensure the last name was submitted
        if not last:
            flash("must provide last name", "warning")
            return redirect("/pay")


        # Ensure the last name fits server-side
        if not re.search("^[a-zA-Z 0-9]{1,100}$", last):
            flash("Invalid last name", "danger")
            return redirect("/pay")


        # Ensure the caresof name fits server-side
        if not re.search("^[a-zA-Z 0-9/]{1,100}$", caresof):
            flash("Invalid C/O name", "danger")
            return redirect("/pay")


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


        # Ensure the city was submitted
        if not city:
            flash("must provide a city", "warning")
            return redirect("/pay")


        # Ensure the city name fits server-side
        if not re.search("^[a-zA-Z 0-9]{1,10}$", city):
            flash("Invalid city", "danger")
            return redirect("/pay")


        # Ensure the country was submitted
        if country == "None":
            flash("must provide a country", "warning")
            return redirect("/pay")


        # Ensure the country fits server-side
        if not re.search("^[a-zA-Z 0-9]{1,100}$", country):
            flash("Invalid a country", "danger")
            return redirect("/pay")


        # Insert users informations into the users table
        query = Users.query.filter_by(id=user_id).first()
        query.first = first
        query.last = last
        query.caresof = caresof
        query.street = street
        query.house = house
        query.zipcode = zipcode
        query.city = city
        query.country = country
        query.additional = additional
        query.express = express
        db.session.commit()


        # Flash result & redirect
        flash("Parcel informations saved", "success")
        return redirect("/confirmation")

        

    else:

        countries = ["Austria", "Belgium", "Bulgaria", "Croatia", "Cyprus", "Czechia", "Denmark", "Estonia", "Finland", "France", "Germany", "Greece", "Hungary", "Ireland", "Italy", "Latvia", "Lithuania", "Luxembourg", "Malta", "Netherlands", "Poland", "Portugal", "Romania", "Slovakia", "Slovenia", "Spain", "Sweden"]

    
        return render_template("pay.html", name=getUserName(), picture=getUserPicture(), role=getUserRole(), countries=countries)