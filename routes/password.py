import traceback
import sys

from flask import Blueprint, render_template, redirect, session, request, flash, get_flashed_messages
from werkzeug.security import check_password_hash, generate_password_hash
from application import getUserName, getUserPicture, login_required, confirmed_required, getUserRole, db, Users
from flask_sqlalchemy import SQLAlchemy


# Set Blueprints
password = Blueprint('password', __name__,)


@password.route("/password", methods=["GET", "POST"])
@login_required
@confirmed_required
def passwordFunction():

    # Force flash() to get the messages on the same page as the redirect.
    get_flashed_messages()


    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Get variable
        password = request.form.get("password")
        user_id = session["user_id"]


        # Ensure password was submitted
        if not password:
            flash("Must provide password")
            return redirect("/password")


        # Query database for hash if already exists
        query = Users.query.filter_by(id=user_id).filter_by(hash=generate_password_hash(password)).all()
        if len(query) != 0:
            flash("Password must be new")
            return redirect("/password")


        # Update database with password hash
        query = Users.query.filter_by(id=user_id).first()
        query.hash = generate_password_hash(password)
        db.session.commit()


        # Flash result & redirect
        flash("Password updated")
        return redirect("/profile")

    
    else:

        return render_template("password.html", name=getUserName(), picture=getUserPicture(), role=getUserRole())