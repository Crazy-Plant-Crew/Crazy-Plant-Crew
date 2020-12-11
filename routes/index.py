from flask import Blueprint, render_template, redirect, session

index = Blueprint('index', __name__,)

@index.route("/", methods=["GET", "POST"])
def indexFunction():
    
    return render_template("index.html")