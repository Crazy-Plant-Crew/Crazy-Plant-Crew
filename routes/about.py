import sqlite3
import traceback
import sys

from flask import Blueprint, render_template, redirect, session, request
from application import getUserName, getUserPicture, login_required, confirmed_required, getUserRole, role_required, db


# Set Blueprints
about = Blueprint('about', __name__,)


@about.route("/about", methods=["GET", "POST"])
@login_required
@confirmed_required
def aboutFunction():    

    if request.method == "POST":

        print("about")
    
    return render_template("about.html", name=getUserName(), picture=getUserPicture(), role=getUserRole())