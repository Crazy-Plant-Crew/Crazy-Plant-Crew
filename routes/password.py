import traceback
import sys

from flask import Blueprint, render_template, redirect, session, request, flash, get_flashed_messages
from werkzeug.security import check_password_hash, generate_password_hash
from application import getUserName, getUserPicture, login_required, confirmed_required, getUserRole, db
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

        password = request.form.get("password")

        # Ensure password was submitted
        if not password:
            flash("must provide password")
            return redirect("/password")

        # Update database with password hash
        user_id = session["user_id"]
        
        # Update database with password hash
        db.engine.execute("UPDATE Users SET hash=:hash WHERE id=:user_id;", {"hash": generate_password_hash(password), "user_id": user_id})

        flash("Password updated")
        return redirect("/profile")

    return render_template("password.html", name=getUserName(), picture=getUserPicture(), role=getUserRole())