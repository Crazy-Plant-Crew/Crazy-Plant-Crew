import sqlite3
import traceback
import sys

from flask import Blueprint, render_template, redirect, session, request
from application import getUserName, getUserPicture, login_required, confirmed_required, getUserRole, role_required

# Set Blueprints
history = Blueprint('history', __name__,)

@history.route("/history", methods=["GET", "POST"])
@login_required
@confirmed_required
def historyFunction():    

    if request.method == "POST":

        print("history")
    
    return render_template("history.html", name=getUserName(), picture=getUserPicture(), role=getUserRole())