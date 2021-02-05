import traceback
import sys

from flask import Blueprint, render_template, redirect, session, request
from application import getUserName, getUserPicture, login_required, confirmed_required, getUserRole, role_required, db
from flask_sqlalchemy import SQLAlchemy


# Set Blueprints
faq = Blueprint('faq', __name__,)


@faq.route("/faq", methods=["GET", "POST"])
@login_required
@confirmed_required
def faqFunction():    

    if request.method == "POST":

        print("faq")
    
    return render_template("faq.html", name=getUserName(), picture=getUserPicture(), role=getUserRole())