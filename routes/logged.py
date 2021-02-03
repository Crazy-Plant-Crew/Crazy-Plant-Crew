import traceback
import sys

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


    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        print("Test")

    
    else:

        # Query database for users
        query = Users.query.all()


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