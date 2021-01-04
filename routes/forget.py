import sqlite3
import traceback
import sys
import random
import string

from flask import Blueprint, render_template, redirect, session, request, flash, get_flashed_messages
from werkzeug.security import check_password_hash, generate_password_hash
from application import randomPassword, getUserName, mail
from flask_mail import Message, Mail

# Set Blueprints
forget = Blueprint('forget', __name__,)

@forget.route("/forget", methods=["GET", "POST"])
def forgetFunction():

    # Force flash() to get the messages on the same page as the redirect.
    flash("Please enter your username, press reset and we will send you a new password")
    get_flashed_messages()

    if request.method == "POST":

        username = request.form.get("username")
        password = randomPassword()
        
        # Check if username exists
        try:

            sqliteConnection = sqlite3.connect("database.db")
            cursor = sqliteConnection.cursor()

            # Query database for username
            cursor.execute("SELECT username FROM users WHERE username=:username;", {"username": username})
            record = cursor.fetchall()

            # Check if username exists
            if len(record) == 0:
                flash("Username does not exist")
                return redirect("/forget")

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
            

        # Update database with new password
        try:

            sqliteConnection = sqlite3.connect("database.db")
            cursor = sqliteConnection.cursor()
            
            # Update database with new password
            cursor.execute("UPDATE users SET hash=:hash WHERE username=:username;", {"hash": generate_password_hash(password), "username": username})
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


        # Get the user email address
        try:

            sqliteConnection = sqlite3.connect("database.db")
            cursor = sqliteConnection.cursor()
            
            # Query database for username
            cursor.execute("SELECT email FROM users WHERE username=:username;", {"username": username})
            email = cursor.fetchall()[0][0]

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


        # Send new password to user
        subject = "New password!"
        body = render_template('reset.html', name=username, password=password)
        messsage = Message(subject=subject, recipients=[email], body=body)
        mail.send(messsage)    

        
        return redirect("/signin")


    else:

        return render_template("forget.html")





    
    