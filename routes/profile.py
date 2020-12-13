from flask import Blueprint, render_template, redirect, session

# Set Blueprints
profile = Blueprint('profile', __name__,)

@profile.route("/profile", methods=["GET", "POST"])
def profileFunction():

    return render_template("profile.html")