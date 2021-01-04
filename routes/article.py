import sqlite3
import traceback
import sys

from flask import Blueprint, render_template, redirect, session, request
from application import getUserName, getUserPicture, login_required, confirmed_required, getUserRole, role_required

# Set Blueprints
article = Blueprint('article', __name__,)

@article.route("/article", methods=["GET", "POST"])
@login_required
@confirmed_required
def articleFunction():    

    if request.method == "POST":

        print("article")
    
    return render_template("article.html", name=getUserName(), picture=getUserPicture(), role=getUserRole())