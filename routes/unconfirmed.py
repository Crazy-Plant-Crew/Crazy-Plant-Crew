import sqlite3
import traceback
import sys
import re

from flask import Blueprint, render_template, redirect, session, request, flash, get_flashed_messages
from application import profileName, profilePicture, mail
from flask_mail import Message, Mail

# Set Blueprints
unconfirmed = Blueprint('unconfirmed', __name__,)

@unconfirmed.route("/unconfirmed", methods=["GET", "POST"])
def unconfirmedFunction():

    # Force flash() to get the messages on the same page as the redirect.
    get_flashed_messages()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        msg = Message(subject="Test email", recipients=["hage.benoit@gmail.com"], body="Testing")
        mail.send(msg)    

        return redirect("/")

    else:

        return render_template("unconfirmed.html", name=profileName(), picture=profilePicture())