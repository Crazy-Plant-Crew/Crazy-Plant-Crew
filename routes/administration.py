import sqlite3
import traceback
import sys

from flask import Blueprint, render_template, redirect, session, request
from application import getUserName, getUserPicture, login_required, confirmed_required, role_required, getUserRole

# Set Blueprints
administration = Blueprint('administration', __name__,)

@administration.route("/administration", methods=["GET", "POST"])
@login_required
@confirmed_required
@role_required
def administrationFunction():    

    if request.method == "POST":

        print("administration")
    
    return render_template("administration.html", name=getUserName(), picture=getUserPicture(), role=getUserRole())