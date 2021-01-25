import traceback
import sys

from flask import Blueprint, render_template, redirect, session, request, flash, get_flashed_messages
from application import getUserName, getUserPicture, login_required, confirmed_required, getUserRole, db
from flask_sqlalchemy import SQLAlchemy

# Set Blueprints
delete = Blueprint('delete', __name__,)

@delete.route("/delete", methods=["GET", "POST"])
@login_required
@confirmed_required
def emailFunction():

    # Force flash() to get the messages on the same page as the redirect.
    get_flashed_messages()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Query database for user id to delete it 
        user_id = session["user_id"]    
        db.engine.execute("DELETE FROM Users WHERE id=:user_id;", {"user_id": user_id})

        flash("Account deleted")
        return redirect("/signin")

    else:

        return render_template("delete.html", name=getUserName(), picture=getUserPicture(), role=getUserRole())