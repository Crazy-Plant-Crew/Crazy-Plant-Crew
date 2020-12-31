import sqlite3
import traceback
import sys

from flask import Blueprint, render_template, redirect, session, request, flash, get_flashed_messages

# Set Blueprints
forget = Blueprint('forget', __name__,)

@forget.route("/forget", methods=["GET", "POST"])
def forgetFunction():

    # Force flash() to get the messages on the same page as the redirect.
    flash("Please enter your username. If you have forgotten it, check your registration email. Press reset and we will send you a new password")
    get_flashed_messages()

    print("forget")
    
    return render_template("forget.html")