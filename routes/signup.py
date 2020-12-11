from flask import Blueprint, render_template, redirect, session

signup = Blueprint('signup', __name__,)

@signup.route("/signup", methods=["GET", "POST"])
def registerFunction():
    
    return render_template("signup.html")