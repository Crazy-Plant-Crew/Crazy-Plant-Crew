import traceback
import sys
import html2text
import os

from flask import Blueprint, render_template, redirect, session, request, flash, get_flashed_messages
from application import getUserName, getUserPicture, login_required, confirmed_required, getUserRole, role_required, sendMail, db
from flask_mail import Message, Mail
from flask_ckeditor import CKEditor
from flask_sqlalchemy import SQLAlchemy

# Set Blueprints
newsletter = Blueprint('newsletter', __name__,)

@newsletter.route("/newsletter", methods=["GET", "POST"])
@login_required
@confirmed_required
@role_required
def newsletterFunction():

    # Force flash() to get the messages on the same page as the redirect.
    get_flashed_messages()


    if request.method == "POST":

        # Get variables
        subject = request.form.get("subject")
        html = request.form.get("ckeditor")
        text = html2text.html2text(html)
        address = request.form.get("address")
        newsletter = request.form.get("newsletter")

        # Query database for user emails for newsletter 
        status = "True"

        record = db.engine.execute("SELECT email FROM Users WHERE newsletter=:newsletter;", {"newsletter": status})
        email = record.fetchall()


        if address != "" and newsletter == None:

            # Send email (subject, email, body)
            sendMail(subject, address, text)
            flash("Single email sent")

        elif address == "" and newsletter == newsletter:

            # Loop through email list and send 
            index  = 0
            while index < len(email):
                sendMail(subject, email[index][0], text)
                index += 1
                
            # Send a copy to Glenn
            sendMail(subject, os.environ["EMAIL_SEND"], text)
            flash("Group email sent")

        else:

            flash("Error: either to one address or select Send Newsletter and leave address blank")
            return redirect("/newsletter")

        return redirect("/")
    
    else:

        return render_template("newsletter.html", name=getUserName(), picture=getUserPicture(), role=getUserRole())