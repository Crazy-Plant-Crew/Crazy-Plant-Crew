import sqlite3
import traceback
import sys

from flask import Blueprint, render_template, redirect, session, request


# Set Blueprints
username = Blueprint('username', __name__,)

@username.route("/username", methods=["GET", "POST"])
def usernameFunction():

    return render_template("username.html")