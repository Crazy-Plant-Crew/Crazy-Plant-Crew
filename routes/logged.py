import traceback
import sys
import os

from flask import Blueprint, render_template, redirect, session, request, flash, get_flashed_messages
from application import getUserName, getUserPicture, login_required, confirmed_required, getUserRole, role_required, db, Users
from flask_sqlalchemy import SQLAlchemy


# Set Blueprints
logged = Blueprint('logged', __name__,)


@logged.route("/logged", methods=["GET", "POST"])
@login_required
@confirmed_required
@role_required
def loggedFunction():    

    # Force flash() to get the messages on the same page as the redirect.
    get_flashed_messages()


    # Query database for users
    query = Users.query.all()


    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Get variable
        remove = request.form.get("remove")
        promote = request.form.get("promote")
        demote = request.form.get("demote")


        if "remove" in request.form:

            # Loop through the DB query
            index = 0
            while index < len(query):

                # Check if field is not empty
                if remove == "":
                    flash("Must provide name REMOVE", "warning")
                    return redirect("/logged")


                # Check if it is root
                elif query[index].username == os.environ.get("USERNAME"):
                    flash("Can't remove this user", "warning")
                    return redirect("/logged")


                # Check if it is the user itself
                elif query[index].id == session["user_id"]:
                    flash("Can't remove yourself", "warning")
                    return redirect("/logged")


                # Check if it is the user is an admin
                elif query[index].role == "admin":
                    flash("Can't remove admin", "warning")
                    return redirect("/logged")


                # Check if the name matches
                elif Users.query.filter_by(username=remove).first() == None:
                    flash("No matching name", "warning")
                    return redirect("/logged")


                # Update database by removing user
                else:
                    Users.query.filter(Users.username == remove).delete()
                    db.session.commit()
                    flash("User deleted", "success")
                    return redirect("/logged")


            index += 1



        if "promote" in request.form:

            # Loop through the DB query
            index = 0
            while index < len(query):

                # Check if field is not empty
                if promote == "":
                    flash("Must provide name PROMOTE", "warning")
                    return redirect("/logged")


                # Check if it is the user is already an admin
                elif query[index].role == "admin":
                    flash("Already admin", "warning")
                    return redirect("/logged")


                # Check if the name matches
                elif Users.query.filter_by(username=promote).first() == None:
                    flash("No matching name", "warning")
                    return redirect("/logged")


                # Update database by promoting user
                else:
                    query = Users.query.filter_by(username=promote).first()
                    query.role = "admin"
                    db.session.commit()
                    flash("User promoted", "success")
                    return redirect("/logged")


            index += 1



        if "demote" in request.form:

            # Loop through the DB query
            index = 0
            while index < len(query):

                # Check if field is not empty
                if demote == "":
                    flash("Must provide name DEMOTE", "warning")
                    return redirect("/logged")


                # Check if it is root
                elif query[index].username == os.environ.get("USERNAME"):
                    flash("Can't demote this user", "warning")
                    return redirect("/logged")


                # Check if it is the user itself
                elif query[index].id == session["user_id"]:
                    flash("Can't demote yourself", "warning")
                    return redirect("/logged")


                # Check if the name matches
                elif Users.query.filter_by(username=demote).first() == None:
                    flash("No matching name", "warning")
                    return redirect("/logged")


                # Update database by demoting user
                else:
                    query = Users.query.filter_by(username=demote).first()
                    query.role = "user"
                    db.session.commit()
                    flash("Admin demoted", "success")
                    return redirect("/logged")


            index += 1
                
    
    else:

        # Set variable
        users = []
        admins = []
        unconfirmeds = []
        index = 0
        
        # Loop through the DB query
        while index < len(query):

            # Users list
            if query[index].role == "user":
                users.extend([[query[index].username, query[index].email]])


            # Admins list
            if query[index].role == "admin":
                admins.extend([query[index].username])


            # Unconfirmeds list
            if query[index].confirmed == "False":
                unconfirmeds.extend([query[index].username])

            index += 1


        return render_template("logged.html", name=getUserName(), picture=getUserPicture(), role=getUserRole(), users=users, admins=admins, unconfirmeds=unconfirmeds)