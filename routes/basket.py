import sqlite3
import traceback
import sys

from flask import Blueprint, render_template, redirect, session, request
from application import getUserName, getUserPicture, login_required, confirmed_required, getUserRole, role_required

# Set Blueprints
basket = Blueprint('basket', __name__,)

@basket.route("/basket", methods=["GET", "POST"])
@login_required
@confirmed_required
def basketFunction():    

    if request.method == "POST":

        print("basket")
    
    return render_template("basket.html", name=getUserName(), picture=getUserPicture(), role=getUserRole())