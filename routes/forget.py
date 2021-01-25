import traceback
import sys
import random
import string

from flask import Blueprint, render_template, redirect, session, request, flash, get_flashed_messages
from werkzeug.security import check_password_hash, generate_password_hash
from application import randomPassword, getUserName, mail, db
from flask_mail import Message, Mail
from flask_sqlalchemy import SQLAlchemy

# Set Blueprints
forget = Blueprint('forget', __name__,)

@forget.route("/forget", methods=["GET", "POST"])
def forgetFunction():

    # Force flash() to get the messages on the same page as the redirect.
    flash("Please enter your username, press reset and we will send you a new password")
    get_flashed_messages()

    if request.method == "POST":

        username = request.form.get("username")
        password = randomPassword()
        
        # Check if username exists
        record = db.engine.execute("SELECT username FROM Users WHERE username=:username;", {"username": username})
        query = record.fetchall()

        if len(query) == 0:
            flash("Username does not exist")
            return redirect("/forget")

        # Update database with new password
        db.engine.execute("UPDATE Users SET hash=:hash WHERE username=:username;", {"hash": generate_password_hash(password), "username": username})

        # Get the user email address
        record = db.engine.execute("SELECT email FROM Users WHERE username=:username;", {"username": username})
        email = record.fetchall()[0][0]

        # Send new password to user
        subject = "New password!"
        body = render_template('reset.html', name=username, password=password)
        messsage = Message(subject=subject, recipients=[email], body=body)
        mail.send(messsage)    

        
        return redirect("/signin")


    else:

        return render_template("forget.html")





    
    