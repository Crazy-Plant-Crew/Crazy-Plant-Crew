import traceback
import sys

from flask import Blueprint, render_template, redirect, session, request
from application import getUserName, getUserPicture, login_required, confirmed_required, getUserRole, db
from flask_sqlalchemy import SQLAlchemy


# Set Blueprints
profile = Blueprint('profile', __name__,)


@profile.route("/profile")
@login_required
@confirmed_required
def profileFunction():
    
    return render_template("profile.html", name=getUserName(), picture=getUserPicture(), role=getUserRole())