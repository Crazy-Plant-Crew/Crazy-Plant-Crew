import sqlite3
import traceback
import sys

from flask import Blueprint, render_template, redirect, session, request
from application import getUserName, getUserPicture, login_required, confirmed_required, getUserRole, role_required

# Set Blueprints
add = Blueprint('add', __name__,)

@add.route("/add", methods=["GET", "POST"])
@login_required
@confirmed_required
@role_required
def addFunction():    

    if request.method == "POST":

        print("add")
    
    return render_template("add.html", name=getUserName(), picture=getUserPicture(), role=getUserRole())