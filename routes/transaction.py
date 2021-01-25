import traceback
import sys

from flask import Blueprint, render_template, redirect, session, request
from application import getUserName, getUserPicture, login_required, confirmed_required, getUserRole, role_required, db
from flask_sqlalchemy import SQLAlchemy

# Set Blueprints
transaction = Blueprint('transaction', __name__,)

@transaction.route("/transaction", methods=["GET", "POST"])
@login_required
@confirmed_required
def transactionFunction():    

    if request.method == "POST":

        print("transaction")
    
    return render_template("transaction.html", name=getUserName(), picture=getUserPicture(), role=getUserRole())