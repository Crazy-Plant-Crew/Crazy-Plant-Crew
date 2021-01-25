import traceback
import sys

from flask import Blueprint, render_template, redirect, session, request, flash, get_flashed_messages
from application import getUserName, getUserPicture, login_required, confirmed_required, getUserRole, db
from flask_sqlalchemy import SQLAlchemy

# Set Blueprints
mailing = Blueprint('mailing', __name__,)

@mailing.route("/mailing", methods=["GET", "POST"])
@login_required
@confirmed_required
def mailingFunction():   

    # Force flash() to get the messages on the same page as the redirect.
    get_flashed_messages() 

    if request.method == "POST":

        if request.form.get('activate'):

            # Update database with newsletter preference
            user_id = session["user_id"]
            newsletter = "True"
            
            # Update database with newsletter
            db.engine.execute("UPDATE Users SET newsletter=:newsletter WHERE id=:user_id;", {"newsletter": newsletter, "user_id": user_id})

        if request.form.get('deactivate'):

            # Update database with newsletter preference
            user_id = session["user_id"]
            newsletter = "False"

            db.engine.execute("UPDATE Users SET newsletter=:newsletter WHERE id=:user_id;", {"newsletter": newsletter, "user_id": user_id})
            
        flash("Newsletter updated")
        return redirect("/profile")

    else:
    
        return render_template("mailing.html", name=getUserName(), picture=getUserPicture(), role=getUserRole())