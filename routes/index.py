import sqlite3
import traceback
import sys

from flask import Blueprint, render_template, redirect, session, request
from application import profileName, profilePicture

# Set Blueprints
index = Blueprint('index', __name__,)

@index.route("/", methods=["GET", "POST"])
def indexFunction():

    if request.method == "POST":

        print("index")
    
    return render_template("index.html", name=profileName(), picture=profilePicture())