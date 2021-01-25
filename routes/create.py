import traceback
import sys
import html2text

from flask import Blueprint, render_template, redirect, session, request, flash, get_flashed_messages
from application import getUserName, getUserPicture, login_required, confirmed_required, getUserRole, role_required, db
from flask_ckeditor import CKEditor
from flask_sqlalchemy import SQLAlchemy

# Set Blueprints
create = Blueprint('create', __name__,)

@create.route("/create", methods=["GET", "POST"])
@role_required
@login_required
@confirmed_required
def createFunction():

    # Force flash() to get the messages on the same page as the redirect.
    get_flashed_messages()  

    if request.method == "POST":

        # Get variable
        title = request.form.get("title")
        body = request.form.get("ckeditor")

        # Insert title and body into the table            
        db.engine.execute("INSERT INTO News(title, body) VALUES (:title, :body)", {"title": title, "body": body})

        flash("News created")
        return redirect("/communication")

    else:
    
        return render_template("create.html", name=getUserName(), picture=getUserPicture(), role=getUserRole())