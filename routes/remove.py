import sqlite3
import traceback
import sys

from flask import Blueprint, render_template, redirect, session, request
from application import getUserName, getUserPicture, login_required, confirmed_required, getUserRole, role_required

# Set Blueprints
remove = Blueprint('remove', __name__,)

@remove.route("/remove", methods=["GET", "POST"])
@login_required
@confirmed_required
@role_required
def removeFunction():    

    if request.method == "POST":

        print("remove")
    
    return render_template("remove.html", name=getUserName(), picture=getUserPicture(), role=getUserRole())