import sqlite3
import traceback
import sys

from flask import Blueprint, render_template, redirect, session, request
from application import getUserName, getUserPicture, login_required, confirmed_required, getUserRole, role_required

# Set Blueprints
newsletter = Blueprint('newsletter', __name__,)

@newsletter.route("/newsletter", methods=["GET", "POST"])
@login_required
@confirmed_required
@role_required
def newsletterFunction():    

    if request.method == "POST":

        print("newsletter")
    
    return render_template("newsletter.html", name=getUserName(), picture=getUserPicture(), role=getUserRole())