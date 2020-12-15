import sqlite3
import traceback
import sys

from flask import Blueprint, render_template, redirect, session, request


# Set Blueprints
email = Blueprint('email', __name__,)

@email.route("/email", methods=["GET", "POST"])
def emailFunction():

    return render_template("email.html")