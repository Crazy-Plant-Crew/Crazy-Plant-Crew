import sqlite3
import traceback
import sys

from flask import Blueprint, render_template, redirect, session, request
from application import profileName, profilePicture, login_required, check_confirmed

# Set Blueprints
message = Blueprint('message', __name__,)

@message.route("/message", methods=["GET", "POST"])
@login_required
@check_confirmed
def messageFunction():    

    if request.method == "POST":

        print("message")
    
    return render_template("message.html", name=profileName(), picture=profilePicture())