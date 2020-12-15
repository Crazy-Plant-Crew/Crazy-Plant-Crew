import sqlite3
import traceback
import sys

from flask import Blueprint, render_template, redirect, session, request


# Set Blueprints
picture = Blueprint('picture', __name__,)

@picture.route("/picture", methods=["GET", "POST"])
def emailFunction():

    return render_template("picture.html")