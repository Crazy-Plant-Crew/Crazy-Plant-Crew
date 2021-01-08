import sqlite3
import traceback
import sys

from flask import Blueprint, render_template, redirect, session, request
from application import getUserName, getUserPicture, login_required, confirmed_required, getUserRole, role_required

# Set Blueprints
create = Blueprint('create', __name__,)

@create.route("/create", methods=["GET", "POST"])
@login_required
@confirmed_required
def createFunction():    

    if request.method == "POST":

        print("create")
    
    return render_template("create.html", name=getUserName(), picture=getUserPicture(), role=getUserRole())