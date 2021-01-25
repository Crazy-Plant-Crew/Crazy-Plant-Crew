import traceback
import sys

from flask import Blueprint, render_template, redirect, session, request, flash, get_flashed_messages, url_for
from application import getUserName, getUserPicture, login_required, confirmed_required, role_required, getUserRole, db
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
    record = db.engine.execute("SELECT * FROM Plants;")
    plants = record.fetchall()


    if request.method == "POST":

        if "delete" in request.form:
        
            # Loop through the record list to match plant ID when delete button is pressed
            index = 0
            while index < len(plants):

                if int(request.form["delete"]) == int(plants[index][0]):

                    # Query database for plant id to delete row
                    plant_id = plants[index][0]
                        
                    db.engine.execute("DELETE FROM Plants WHERE id=:id;", {"id": plant_id})

                    flash("Plant deleted")
                    return redirect("/administration")

                else:

                    index += 1


        if "edit" in request.form:   

            # Loop through the record list to match plant ID when edit button is pressed
            index = 0
            while index < len(plants):

                if int(request.form["edit"]) == int(plants[index][0]):

                    thisPlant = plants[index]

                    return redirect(url_for("edit.editFunction", plants=thisPlant))

                else:

                    index += 1

    else:
   
        return render_template("administration.html", name=getUserName(), picture=getUserPicture(), role=getUserRole(), plants=plants)