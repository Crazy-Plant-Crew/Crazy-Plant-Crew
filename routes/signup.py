import traceback
import sys
import os
import re

from flask import Blueprint, render_template, redirect, session, request, flash, get_flashed_messages
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename
from application import uploadPicture, is_human, sendPin, allowed_file, db
from time import time
from flask_sqlalchemy import SQLAlchemy


# Set Blueprints
signup = Blueprint('signup', __name__,)

# Assign public key
pub_key = os.environ.get("SITE_KEY")

@signup.route("/signup", methods=["GET", "POST"])
def signupFunction():

    # Force flash() to get the messages on the same page as the redirect.
    get_flashed_messages()

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        email = request.form.get("email")
        username = request.form.get("username")
        password = request.form.get("password")
        confirmPassword  = request.form.get("confirm-password")
        captcha_response = request.form['g-recaptcha-response']

        # token = generate_confirmation_token(email)

        # Ensure captcha was correct
        if is_human(captcha_response) != True:
            flash("must completed captcha")
            return redirect("/signup")

            
        # Ensure email was submitted
        if not email:
            flash("must provide email")
            return redirect("/signup")

        # Ensure username was submitted
        if not username:
            flash("must provide username")
            return redirect("/signup")

        # Ensure password was submitted
        if not password:
            flash("must provide password")
            return redirect("/signup")

        # Ensure confirm password is correct
        if password != confirmPassword:
            flash("The passwords don't match")
            return redirect("/signup")

        # Ensure username fits server-side
        if not re.search("^[a-zA-Z0-9]{2,20}$", username):
            flash("Invalid username")
            return redirect("/signup")

        # Ensure email fits server-side
        if not re.search(r"[^@]+@[^@]+\.[^@]+", email):
            flash("Invalid email")
            return redirect("/signup")


        # Query database for username if already exists
        record = db.engine.execute("SELECT * FROM Users WHERE username=:username;", {"username": username})
        query = cursor.fetchall()

        # Check if username is free
        if len(query) != 0:
            flash("Username already taken")
            return redirect("/signup")


        # Query database for email if already exists
        record = db.engine.execute("SELECT * FROM Users WHERE email=:email;", {"email": email})
        query = record.fetchall()

        # Check if email is free
        if len(query) != 0:
            flash("Email already taken")
            return redirect("/signup")
            

        # Insert username, email and hash of the password into the table
        db.engine.execute("INSERT INTO Users(username, hash, email) VALUES (:username, :hash, :email)", {"username": username, "hash": generate_password_hash(password), "email": email})

        # Query database for username & remember which user has logged in
        record = db.engine.execute("SELECT * FROM Users WHERE username=:username;", {"username": username})
        query = record.fetchall()
        
        # Remember which user has logged in
        session["user_id"] = query[0][0]

        
        # Save, upload and delete picture file
        file = request.files["picture"]

        if file and allowed_file(file.filename):

            filename = secure_filename(file.filename)
            file.save(os.path.join("./static", filename))
            upload = uploadPicture("./static/" + filename)
            os.remove("./static/" + filename)

            # Update database with new image url 
            user_id = session["user_id"]  
            db.engine.execute("UPDATE Users SET picture=:picture WHERE id=:id;", {"picture": upload, "id": user_id})

        
        sendPin(email)

        return redirect("/")

    
    # User reached route via GET (as by clicking a link or via redirect)
    else:

        return render_template("signup.html", pub_key=pub_key)

