import sqlite3
import traceback
import sys
import html2text

from flask import Blueprint, render_template, redirect, session, request, flash, get_flashed_messages
from application import getUserName, getUserPicture, login_required, confirmed_required, getUserRole, role_required

# Set Blueprints
change = Blueprint('change', __name__,)

@change.route("/change", methods=["GET", "POST"])
@login_required
@confirmed_required
@role_required
def changeFunction():    

    # Force flash() to get the messages on the same page as the redirect.
    get_flashed_messages()  

    if request.method == "POST":

        # Get variable
        news_id = request.form.get("news_id")
        title = request.form.get("title")
        html = request.form.get("ckeditor")
        body = html2text.html2text(html)

        # Update plant name, stock, price, description and show status into the table
        try:

            sqliteConnection = sqlite3.connect("database.db")
            cursor = sqliteConnection.cursor()

            cursor.execute("UPDATE news SET title=:title, body=:body WHERE id=:id;", {"title": title, "body": body, "id": news_id})
            sqliteConnection.commit()

            cursor.close()

        except sqlite3.Error as error:
        
            print("Failed to read data from sqlite table", error)
            print("Exception class is: ", error.__class__)
            print("Exception is", error.args)

            print('Printing detailed SQLite exception traceback: ')
            exc_type, exc_value, exc_tb = sys.exc_info()
            print(traceback.format_exception(exc_type, exc_value, exc_tb))

        finally:

            if (sqliteConnection):
                sqliteConnection.close()
        
        flash("News edited")
        return redirect("/communication")

    else:

        # Get arguments from url_for in administration
        thisNews = request.args.getlist("news")
    
        return render_template("change.html", name=getUserName(), picture=getUserPicture(), role=getUserRole(), news=thisNews)