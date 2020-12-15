import sqlite3
import traceback
import sys

from flask import Blueprint, render_template, redirect, session, request
from application import profileName

# Set Blueprints
profile = Blueprint('profile', __name__,)

@profile.route("/profile", methods=["GET", "POST"])
def profileFunction():

    if request.method == "POST":

        print("profile")
    
    return render_template("profile.html", name=profileName())