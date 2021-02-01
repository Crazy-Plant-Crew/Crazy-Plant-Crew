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

        query = Users.query.all()
        userList = []
        index = 0
        
        while index < len(query):

            userList.extend([query[index].username])
            index += 1


        return render_template("logged.html", name=getUserName(), picture=getUserPicture(), role=getUserRole(), users=userList)