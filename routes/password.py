import sqlite3
import traceback
import sys

from flask import Blueprint, render_template, redirect, session, request
from application import profileName

# Set Blueprints
password = Blueprint('password', __name__,)

@password.route("/password", methods=["GET", "POST"])
def passwordFunction():

    return render_template("password.html", name=profileName())