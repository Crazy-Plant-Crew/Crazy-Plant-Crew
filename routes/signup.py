import sqlite3
from flask import Blueprint, render_template, redirect, session, request, flash
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from application import database

# Set database
database = database()

# Set Blueprints
signup = Blueprint('signup', __name__,)

@signup.route("/signup", methods=["GET", "POST"])
def signupFunction():

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return flash("must provide username")

        # Ensure password was submitted
        elif not request.form.get("password"):
            return flash("must provide password")

        # Ensure confirm password is correct
        elif request.form.get("password") != request.form.get("confirm-password"):
            return flash("The passwords don't match")

        # Query database for username if already exists
        elif database.execute("SELECT * FROM users WHERE username = :username", username=request.form.get("username")):
            return flash("Username already taken")

        # Insert user and hash of the password into the table
        database.execute("INSERT INTO users(username, hash) VALUES (:username, :hash)", username=request.form.get("username"), hash=generate_password_hash(request.form.get("password")))

        # Query database for username
        rows = database.execute("SELECT * FROM users WHERE username = :username", username=request.form.get("username"))

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Close database connection
        database.close()

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("signup.html")
