from flask import Blueprint, render_template, redirect, session

# Set Blueprints
logout = Blueprint('logout', __name__,)

@logout.route("/logout")
def logoutFunction():
    session.clear()
    return redirect("/signin")