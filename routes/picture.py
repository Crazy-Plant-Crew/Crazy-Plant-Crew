import traceback
import sys
import os

from flask import Blueprint, render_template, redirect, session, request, flash
from application import getUserName, uploadPicture, getUserPicture, login_required, confirmed_required, getUserRole, allowed_file, db, Users
from werkzeug.utils import secure_filename
from flask_sqlalchemy import SQLAlchemy


# Set Blueprints
picture = Blueprint('picture', __name__,)


@picture.route("/picture", methods=["GET", "POST"])
@login_required
@confirmed_required
def pictureFunction():

    # Force flash() to get the messages on the same page as the redirect.
    get_flashed_messages()


    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Save, upload and delete picture file
        file = request.files["picture"]
        if file and allowed_file(file.filename):

            filename = secure_filename(file.filename)
            file.save(os.path.join("./static", filename))
            upload = uploadPicture("./static/" + filename)
            os.remove("./static/" + filename)


            # Update database with new image url 
            user_id = session["user_id"]
            query = Users.query.filter_by(username=username).first()
            query.picture = upload
            db.session.commit()     


        # Flash result & redirect
        flash("Profile picture updated")
        return redirect("/")
        

    else:

        return render_template("picture.html", name=getUserName(), picture=getUserPicture(), role=getUserRole())