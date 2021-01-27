import traceback
import sys
import re

from flask import Blueprint, render_template, redirect, session, request, flash, get_flashed_messages
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from flask_sqlalchemy import SQLAlchemy
from application import db, Users
from sqlalchemy import text

# Set Blueprints
signin = Blueprint('signin', __name__,)

@signin.route("/signin", methods=["GET", "POST"])
def signinFunction():

    # Force flash() to get the messages on the same page as the redirect.
    get_flashed_messages()

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")

        # Ensure username was submitted
        if not username:
            flash("must provide username")
            return redirect("/signin")

        # Ensure username fits server-side
        if not re.search("^[a-zA-Z0-9]{2,20}$", username):
            flash("Invalid username")
            return redirect("/signin")

        # Ensure password was submitted
        if not password:
            flash("must provide password")
            return redirect("/signin")

        # Query database for username if already exists
        query = Users.query.filter_by(username=username).all()

        # Ensure username exists and password is correct
        if query is not None or not check_password_hash(query.hash, password):
            flash("invalid username and/or password")
            return redirect("/signin")

        # Remember which user has logged in
        session["user_id"] = query.id


        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("signin.html")
