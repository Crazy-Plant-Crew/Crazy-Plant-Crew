import sqlite3
import traceback
import sys

from flask import Blueprint, render_template, redirect, session, request
from application import getUserName, getUserPicture, login_required, confirmed_required, getUserRole, role_required

# Set Blueprints
communication = Blueprint('communication', __name__,)

@communication.route("/communication", methods=["GET", "POST"])
@login_required
@confirmed_required
@role_required
def communicationFunction():    

    if request.method == "POST":

        print("communication")
    
    return render_template("communication.html", name=getUserName(), picture=getUserPicture(), role=getUserRole())