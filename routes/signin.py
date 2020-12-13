import sqlite3
from flask import Blueprint, render_template, redirect, session, request, flash
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

# Set Blueprints
signin = Blueprint('signin', __name__,)

@signin.route("/signin", methods=["GET", "POST"])
def signinFunction():

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        
        try:
            username = request.form.get("username")
            password = request.form.get("password")

            with sqlite3.connect("database") as connection:
                print("Opened database successfully")
                current = connection.cursor()

                # Ensure username was submitted
                if not request.form.get("username"):
                    return flash("must provide username")

                # Ensure password was submitted
                elif not request.form.get("password"):
                    return flash("must provide password")

                # Query database for username
                rows = current.execute("SELECT * FROM users WHERE username = :username", username=username)

                # Ensure username exists and password is correct
                if len(rows) != 1 or not check_password_hash(rows[0]["hash"], password):
                    return flash("invalid username and/or password")

                # Remember which user has logged in
                session["user_id"] = rows[0]["id"]

                # Commit to databse
                connection.commit()

                print("Database operation succesful")

        except:
            connection.rollback()
            print("Error in sign in operation")

        finally:
            # Close database connection
            connection.close()
        
            # Redirect user to home page
            return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("signin.html")