from flask import Blueprint, render_template, redirect, session

login = Blueprint('login', __name__,)

@login.route("/login", methods=["GET", "POST"])
def loginFunction():
    
    return render_template("login.html")