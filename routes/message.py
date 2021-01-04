import sqlite3
import traceback
import sys

from flask import Blueprint, render_template, redirect, session, request
from application import getUserName, getUserPicture, login_required, confirmed_required, getUserRole

# Set Blueprints
message = Blueprint('message', __name__,)

@message.route("/message", methods=["GET", "POST"])
@login_required
@confirmed_required
def messageFunction():    

    if request.method == "POST":

        print("message")
    
    return render_template("message.html", name=getUserName(), picture=getUserPicture(), role=getUserRole())