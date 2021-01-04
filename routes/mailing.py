import sqlite3
import traceback
import sys

from flask import Blueprint, render_template, redirect, session, request
from application import getUserName, getUserPicture, login_required, confirmed_required, getUserRole

# Set Blueprints
mailing = Blueprint('mailing', __name__,)

@mailing.route("/mailing", methods=["GET", "POST"])
@login_required
@confirmed_required
def mailingFunction():    

    if request.method == "POST":

        print("mailing")
    
    return render_template("mailing.html", name=getUserName(), picture=getUserPicture(), role=getUserRole())