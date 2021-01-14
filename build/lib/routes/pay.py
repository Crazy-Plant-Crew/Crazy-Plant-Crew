import sqlite3
import traceback
import sys

from flask import Blueprint, render_template, redirect, session, request
from application import getUserName, getUserPicture, login_required, confirmed_required, getUserRole, role_required

# Set Blueprints
pay = Blueprint('pay', __name__,)

@pay.route("/pay", methods=["GET", "POST"])
@login_required
@confirmed_required
def payFunction():    

    if request.method == "POST":

        print("pay")

    else:
    
        return render_template("pay.html", name=getUserName(), picture=getUserPicture(), role=getUserRole())