import sqlite3
import traceback
import sys

from flask import Blueprint, render_template, redirect, session, request
from application import profileName

# Set Blueprints
message = Blueprint('message', __name__,)

@message.route("/message", methods=["GET", "POST"])
def messageFunction():    

    if request.method == "POST":

        print("message")
    
    return render_template("message.html", name=profileName())