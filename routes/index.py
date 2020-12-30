import sqlite3
import traceback
import sys

from flask import Blueprint, render_template, redirect, session, request
from application import profileName, profilePicture, login_required, check_confirmed

# Set Blueprints
index = Blueprint('index', __name__,)

@index.route("/", methods=["GET", "POST"])
@login_required
@check_confirmed
def indexFunction():
    
    return render_template("index.html", name=profileName(), picture=profilePicture())