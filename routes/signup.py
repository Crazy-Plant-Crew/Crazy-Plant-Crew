import sqlite3
from flask import Blueprint, render_template, redirect, session, request, flash
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

# Set Blueprints
signup = Blueprint('signup', __name__,)

@signup.route("/signup", methods=["GET", "POST"])
def signupFunction():

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        try:
            email = request.form.get("email")
            username = request.form.get("username")
            password = request.form.get("password")
            confirmPassword  = request.form.get("confirm-password")

            with sqlite3.connect("database") as connection:
                current = connection.cursor()

                # Ensure email was submitted
                if not email:
                    return flash("must provide email")
                # Ensure username was submitted
                if not username:
                    return flash("must provide username")

                # Ensure password was submitted
                elif not password:
                    return flash("must provide password")

                # Ensure confirm password is correct
                elif password != confirmPassword:
                    return flash("The passwords don't match")

                # Query database for username if already exists
                elif current.execute("SELECT * FROM users WHERE username = :username", username=username):
                    return flash("Username already taken")

                # Insert user and hash of the password into the table
                current.execute("INSERT INTO users(username, hash) VALUES (:username, :hash)", username=username, hash=generate_password_hash(password))

                # Query database for username
                rows = current.execute("SELECT * FROM users WHERE username = :username", username=username)

                # Remember which user has logged in
                session["user_id"] = rows[0]["id"]
            
        except:
            connection.rollback()
            print("Error in sign up operation")
        
        finally:
            # Close database connection
            connection.close()
            # Redirect user to home page
            return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("signup.html")
