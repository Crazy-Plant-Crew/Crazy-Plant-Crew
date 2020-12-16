import sqlite3
import traceback
import sys

from flask import Blueprint, render_template, redirect, session, request
from application import profileName, profilePicture

# Set Blueprints
delete = Blueprint('delete', __name__,)

@delete.route("/delete", methods=["GET", "POST"])
def emailFunction():

    return render_template("delete.html", name=profileName(), picture=profilePicture())