import traceback
import sys
import os

from flask import Blueprint, render_template, redirect, session, request, flash
from application import getUserName, uploadPicture, getUserPicture, login_required, confirmed_required, getUserRole, allowed_file, db
from werkzeug.utils import secure_filename
from flask_sqlalchemy import SQLAlchemy

# Set Blueprints
picture = Blueprint('picture', __name__,)

@picture.route("/picture", methods=["GET", "POST"])
@login_required
@confirmed_required
def pictureFunction():

    if request.method == "POST":

        # check if the post request has the file part
        if "picture" not in request.files:
            flash("No file part")
            return redirect("/picture")

        file = request.files["picture"]

        # if user does not select file, browser also submit a empty part without filename
        if file.filename == "":
            flash("No selected file")
            return redirect("/picture")

        # Check if all conditions are satisfied
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join("./static", filename))
            upload = uploadPicture("./static/" + filename)
            os.remove("./static/" + filename)         

        # Update database with new image url 
        user_id = session["user_id"]
        cursor.execute("UPDATE Users SET picture=:picture WHERE id=:user_id;", {"picture": upload, "user_id": user_id})

        flash("Profile picture updated")
        return redirect("/")

    else:

        return render_template("picture.html", name=getUserName(), picture=getUserPicture(), role=getUserRole())