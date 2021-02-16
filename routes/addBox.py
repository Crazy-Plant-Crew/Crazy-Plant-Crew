import traceback
import sys

from flask import Blueprint, render_template, redirect, session, request
from application import getUserName, getUserPicture, login_required, confirmed_required, getUserRole, role_required, db, Boxes
from flask_sqlalchemy import SQLAlchemy


# Set Blueprints
addBox = Blueprint('addBox', __name__,)


@addBox.route("/addBox", methods=["GET", "POST"])
@login_required
@confirmed_required
def addBoxFunction():    

    if request.method == "POST":

        print("addBox")
    
    return render_template("addBox.html", name=getUserName(), picture=getUserPicture(), role=getUserRole())