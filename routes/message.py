from flask import Blueprint, render_template, redirect, session

message = Blueprint('message', __name__,)

@message.route("/message", methods=["GET", "POST"])
def messageFunction():
    
    return render_template("message.html")