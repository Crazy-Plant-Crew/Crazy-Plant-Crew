import traceback
import sys

from flask import Blueprint, render_template, redirect, session, request, flash, get_flashed_messages
from application import getUserName, getUserPicture, login_required, confirmed_required, getUserRole, role_required, db
from flask_sqlalchemy import SQLAlchemy

# Set Blueprints
article = Blueprint('article', __name__,)

@article.route("/article", methods=["GET", "POST"])
@login_required
@confirmed_required
def articleFunction():

    # Force flash() to get the messages on the same page as the redirect.
    get_flashed_messages()  


    if request.method == "POST":

        return redirect("/")

    else:

        # Query database for news to display them
        record = db.engine.execute("SELECT * FROM News;")
        communications = record.fetchall()

    
        return render_template("article.html", name=getUserName(), picture=getUserPicture(), role=getUserRole(), communications=communications)