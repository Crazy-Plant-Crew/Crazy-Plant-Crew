import sqlite3
import traceback
import sys
import html2text

from flask import Blueprint, render_template, redirect, session, request, flash, get_flashed_messages
from application import getUserName, getUserPicture, login_required, confirmed_required, getUserRole, role_required
from flask_ckeditor import CKEditor

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
        try:

            sqliteConnection = sqlite3.connect("database.db")
            cursor = sqliteConnection.cursor()
            
            cursor.execute("INSERT INTO news(title, body) VALUES (:title, :body)", {"title": title, "body": body})
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

        flash("News created")
        return redirect("/communication")

    else:
    
        return render_template("create.html", name=getUserName(), picture=getUserPicture(), role=getUserRole())