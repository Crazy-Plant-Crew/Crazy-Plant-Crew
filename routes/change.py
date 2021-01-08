import sqlite3
import traceback
import sys

from flask import Blueprint, render_template, redirect, session, request
from application import getUserName, getUserPicture, login_required, confirmed_required, getUserRole, role_required

# Set Blueprints
change = Blueprint('change', __name__,)

@change.route("/change", methods=["GET", "POST"])
@login_required
@confirmed_required
def changeFunction():    

    if request.method == "POST":

        print("change")
    
    return render_template("change.html", name=getUserName(), picture=getUserPicture(), role=getUserRole())