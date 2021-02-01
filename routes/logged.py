import traceback
import sys

from flask import Blueprint, render_template, redirect, session, request
from application import getUserName, getUserPicture, login_required, confirmed_required, getUserRole, role_required, db
from flask_sqlalchemy import SQLAlchemy


# Set Blueprints
logged = Blueprint('logged', __name__,)


@logged.route("/logged", methods=["GET", "POST"])
@login_required
@confirmed_required
@role_required
def loggedFunction():    

    if request.method == "POST":

        print("logged")
    
    return render_template("logged.html", name=getUserName(), picture=getUserPicture(), role=getUserRole())