import traceback
import sys

from flask import Blueprint, render_template, redirect, session, request, flash, get_flashed_messages, url_for
from application import getUserName, getUserPicture, login_required, confirmed_required, getUserRole, role_required, db, News
from flask_sqlalchemy import SQLAlchemy


# Set Blueprints
communication = Blueprint('communication', __name__,)


@communication.route("/communication", methods=["GET", "POST"])
@login_required
@confirmed_required
@role_required
def communicationFunction():

    # Force flash() to get the messages on the same page as the redirect.
    get_flashed_messages() 


    # Query database for news to display them
    news = News.query.all()


    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        if "erase" in request.form:
        
            # Loop through the record list to match plant ID when delete button is pressed
            index = 0
            while index < len(news):

                if int(request.form["erase"]) == int(news[index].id):

                    # Query database for plant id to delete row
                    News.query.filter(News.id == news[index].id).delete()
                    db.session.commit()

                    # Flash result & redirect
                    flash("News deleted")
                    return redirect("/communication")


                else:

                    index += 1


        if "change" in request.form:   

            # Loop through the record list to match plant ID when edit button is pressed
            index = 0
            while index < len(news):

                if int(request.form["change"]) == int(news[index].id):

                    # Create a list with values of DB and append them
                    thisNews = []
                    thisNews.extend([news[index].id, news[index].title, news[index].body)

                    return redirect(url_for("change.changeFunction", news=thisNews))

                else:

                    index += 1


    else:
    
        return render_template("communication.html", name=getUserName(), picture=getUserPicture(), role=getUserRole(), news=news)