import sqlite3
import traceback
import sys

from flask import Blueprint, render_template, redirect, session, request
from application import getUserName, getUserPicture, login_required, confirmed_required, getUserRole, role_required

# Set Blueprints
edit = Blueprint('edit', __name__,)

@edit.route("/edit", methods=["GET", "POST"])
@login_required
@confirmed_required
@role_required
def editFunction():    

    if request.method == "POST":

        print("edit")
    
    return render_template("edit.html", name=getUserName(), picture=getUserPicture(), role=getUserRole())