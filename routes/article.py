import traceback
import sys

from flask import Blueprint, render_template, redirect, session, request, flash, get_flashed_messages
from application import getUserName, getUserPicture, login_required, confirmed_required, getUserRole, role_required, db, News
from flask_sqlalchemy import SQLAlchemy


# Set Blueprints
article = Blueprint('article', __name__,)


@article.route("/article", methods=["GET", "POST"])
@login_required
@confirmed_required
def articleFunction():

    # Force flash() to get the messages on the same page as the redirect.
    get_flashed_messages()  


    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        return redirect("/")

    else:
        
        query = News.query.all()
        index = 0

        while index < len(query):

            # Create a list with values of DB and append them
            news = []
            news.extend([query[index]])
            print(news)
    
        return render_template("article.html", name=getUserName(), picture=getUserPicture(), role=getUserRole(), news=news)