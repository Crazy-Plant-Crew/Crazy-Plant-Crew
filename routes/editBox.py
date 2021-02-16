import traceback
import sys

from flask import Blueprint, render_template, redirect, session, request
from application import getUserName, getUserPicture, login_required, confirmed_required, getUserRole, role_required, db, Boxes
from flask_sqlalchemy import SQLAlchemy


# Set Blueprints
editBox = Blueprint('editBox', __name__,)


@editBox.route("/editBox", methods=["GET", "POST"])
@login_required
@confirmed_required
@role_required
def editBoxFunction():    

    if request.method == "POST":

        print("editBox")
    
    return render_template("editBox.html", name=getUserName(), picture=getUserPicture(), role=getUserRole())