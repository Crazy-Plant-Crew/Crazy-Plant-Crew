import sqlite3
import traceback
import sys

from flask import Blueprint, render_template, redirect, session, request
from application import profileName, profilePicture, login_required, check_confirmed

# Set Blueprints
profile = Blueprint('profile', __name__,)

@profile.route("/profile")
@login_required
@check_confirmed
def profileFunction():
    
    return render_template("profile.html", name=profileName(), picture=profilePicture())