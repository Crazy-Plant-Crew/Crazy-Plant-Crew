import traceback
import sys

from flask import Blueprint, render_template, redirect, session, request, flash, get_flashed_messages
from application import getUserName, getUserPicture, login_required, confirmed_required, getUserRole, db, Users
from flask_sqlalchemy import SQLAlchemy


# Set Blueprints
mailing = Blueprint('mailing', __name__,)


@mailing.route("/mailing", methods=["GET", "POST"])
@login_required
@confirmed_required
def mailingFunction():   

    # Force flash() to get the messages on the same page as the redirect.
    get_flashed_messages() 


    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Get variable
        user_id = session["user_id"]


        # Activate newsletter and update DB
        if request.form.get('activate'):

            newsletter = "True"
            query = Users.query.filter_by(id=user_id).first()
            query.newsletter = newsletter
            db.session.commit()


        # Deactivate newsletter and update DB
        if request.form.get('deactivate'):

            newsletter = "False"
            query = Users.query.filter_by(id=user_id).first()
            query.newsletter = newsletter
            db.session.commit()


        # Flash result & redirect    
        flash("Newsletter updated", "success")
        return redirect("/profile")


    else:
    
        return render_template("mailing.html", name=getUserName(), picture=getUserPicture(), role=getUserRole())