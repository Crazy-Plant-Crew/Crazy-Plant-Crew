import sqlite3
import traceback
import sys
import os
import html2text

from flask import Blueprint, render_template, redirect, session, request, flash, get_flashed_messages
from application import getUserName, getUserPicture, login_required, confirmed_required, getUserRole, getUserEmail, sendMail
from flask_mail import Message, Mail
from flask_ckeditor import CKEditor

# Set Blueprints
message = Blueprint('message', __name__,)

@message.route("/message", methods=["GET", "POST"])
@login_required
@confirmed_required
def messageFunction():    

    if request.method == "POST":

        subject = "Message from " + getUserName()
        html = request.form.get("ckeditor")
        text = html2text.html2text(html)
        body = "Username: " + getUserName() + "\nEmail: " + getUserEmail() + "\n\nMessage: " + text
        email = os.environ["EMAIL_SEND"]

        sendMail(subject, email, body)

        flash("Message sent")
        return redirect("/")

    else:
    
        return render_template("message.html", name=getUserName(), picture=getUserPicture(), role=getUserRole())