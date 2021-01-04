import sqlite3
import traceback
import sys

from flask import Blueprint, render_template, redirect, session, request
from application import getUserName, getUserPicture, getUserRole, login_required, confirmed_required

# Set Blueprints
index = Blueprint('index', __name__,)

@index.route("/", methods=["GET", "POST"])
@login_required
@confirmed_required
def indexFunction():

    return render_template("index.html", name=getUserName(), picture=getUserPicture(), role=getUserRole())