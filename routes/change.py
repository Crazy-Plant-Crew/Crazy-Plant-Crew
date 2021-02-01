import traceback
import sys
import html2text

from flask import Blueprint, render_template, redirect, session, request, flash, get_flashed_messages
from application import getUserName, getUserPicture, login_required, confirmed_required, getUserRole, role_required, db, News
from flask_sqlalchemy import SQLAlchemy


# Set Blueprints
change = Blueprint('change', __name__,)


@change.route("/change", methods=["GET", "POST"])
@login_required
@confirmed_required
@role_required
def changeFunction():    

    # Force flash() to get the messages on the same page as the redirect.
    get_flashed_messages()  
    
    
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Get variable
        news_id = request.form.get("news_id")
        title = request.form.get("title")
        html = request.form.get("ckeditor")
        body = html2text.html2text(html)


        # Update plant name, stock, price, description and show status into the table
        db.engine.execute("UPDATE News SET title=:title, body=:body WHERE id=:id;", {"title": title, "body": body, "id": news_id})
        query = News.query.filter_by(id=news_id).first()
        query.title = title
        query.body = body
        db.session.commit()
        

        # Flash result & redirect
        flash("News edited", "Information")
        return redirect("/communication")


    else:

        # Get arguments from url_for in administration
        thisNews = request.args.getlist("news")
    
        return render_template("change.html", name=getUserName(), picture=getUserPicture(), role=getUserRole(), news=thisNews)