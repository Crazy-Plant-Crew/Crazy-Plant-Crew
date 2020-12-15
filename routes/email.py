import sqlite3
import traceback
import sys

from flask import Blueprint, render_template, redirect, session, request
from application import profileName

# Set Blueprints
email = Blueprint('email', __name__,)

@email.route("/email", methods=["GET", "POST"])
def emailFunction():

    return render_template("email.html", name=profileName())