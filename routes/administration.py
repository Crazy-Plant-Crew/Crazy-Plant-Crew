import traceback
import sys

from flask import Blueprint, render_template, redirect, session, request, flash, get_flashed_messages, url_for
from application import getUserName, getUserPicture, login_required, confirmed_required, role_required, getUserRole, db, Plants
from flask_sqlalchemy import SQLAlchemy


# Set Blueprints
administration = Blueprint('administration', __name__,)


@administration.route("/administration", methods=["GET", "POST"])
@login_required
@confirmed_required
@role_required
def administrationFunction():

    # Force flash() to get the messages on the same page as the redirect.
    get_flashed_messages()


    # Query database for plants
    plants = Plants.query.all()


    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        if "delete" in request.form:
        
            # Loop through the record list to match plant ID when delete button is pressed
            index = 0
            while index < len(plants):

                if int(request.form["delete"]) == int(plants[index].id):

                    # Query database for plant id to delete row
                    Plants.query.filter(Plants.id == plants[index].id).delete()
                    db.session.commit()

                    # Flash result & redirect
                    flash("Plant deleted", "success")
                    return redirect("/administration")

                else:

                    index += 1


        if "edit" in request.form:   

            # Loop through the record list to match plant ID when edit button is pressed
            index = 0
            while index < len(plants):

                if int(request.form["edit"]) == int(plants[index].id):

                    # Create a list with values of DB and append them
                    thisPlant = []
                    thisPlant.extend([plants[index].id, plants[index].name, plants[index].stock, plants[index].price, plants[index].picture, plants[index].description, plants[index].show])

                    return redirect(url_for("edit.editFunction", plants=thisPlant))

                else:

                    index += 1


    else:
   
        return render_template("administration.html", name=getUserName(), picture=getUserPicture(), role=getUserRole(), plants=plants)