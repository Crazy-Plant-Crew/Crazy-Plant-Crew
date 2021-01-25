import traceback
import sys
import re

from flask import Blueprint, render_template, redirect, session, request, flash, get_flashed_messages
from application import getUserName, getUserPicture, login_required, confirmed_required, getUserRole, db
from flask_sqlalchemy import SQLAlchemy

# Set Blueprints
username = Blueprint('username', __name__,)

@username.route("/username", methods=["GET", "POST"])
@login_required
@confirmed_required
def usernameFunction():

    # Force flash() to get the messages on the same page as the redirect.
    get_flashed_messages()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        username = request.form.get("username")

        # Ensure username was submitted
        if not username:
            flash("must provide username")
            return redirect("/username")

        # Ensure username fits server-side
        if not re.search("^[a-zA-Z0-9]{2,20}$", username):
            flash("Invalid username")
            return redirect("/username")


        # Query database for username if already exists
        record = db.engine.execute("SELECT * FROM Users WHERE username=:username;", {"username": username})
        query = record.fetchall()

        # Check if username is free
        if len(query) != 1:
            flash("Username already taken")
            return redirect("/username")


        # Update database with username

        user_id = session["user_id"]
        db.engine.execute("UPDATE Users SET username=:username WHERE id=:user_id;", {"username": username, "user_id": user_id})

        flash("Username updated")
        return redirect("/profile")
    
    else:

        return render_template("username.html", name=getUserName(), picture=getUserPicture(), role=getUserRole())