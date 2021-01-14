import sqlite3
import traceback
import sys

from flask import Blueprint, render_template, redirect, session, request, flash, get_flashed_messages
from application import getUserName, getUserPicture, getUserRole, login_required, confirmed_required

# Set Blueprints
index = Blueprint('index', __name__,)

@index.route("/", methods=["GET", "POST"])
@login_required
@confirmed_required
def indexFunction():

    # Force flash() to get the messages on the same page as the redirect.
    get_flashed_messages()


    if request.method == "POST":


        # Get variables
        plant_id = request.form.get("plant_id")
        user_id = session["user_id"]
        quantity = request.form.get("quantity")


        # Query database for plants name, picture, price
        try:

            sqliteConnection = sqlite3.connect("database.db")
            cursor = sqliteConnection.cursor()
            
            # Query database
            cursor.execute("SELECT * FROM plants WHERE id=:id;", {"id": plant_id})
            plants = cursor.fetchall()
            name = plants[0][1]
            picture = plants[0][4]
            price = plants[0][3]

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
       

        # Get current plant stock
        try:

            sqliteConnection = sqlite3.connect("database.db")
            cursor = sqliteConnection.cursor()
            
            # Query database
            cursor.execute("SELECT stock FROM plants WHERE id=:id;", {"id": plant_id})
            existingStock = cursor.fetchall()

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


        # Avoid going to negative stocks
        if len(existingStock) != 0:
            if int(existingStock[0][0]) - int(quantity) < 0:

                flash("Not enough in stock")
                return redirect("/")

        
        # Check for existing stock in the basket
        try:

            sqliteConnection = sqlite3.connect("database.db")
            cursor = sqliteConnection.cursor()
            
            # Query database
            cursor.execute("SELECT quantity FROM baskets WHERE plant_id=:plant_id AND user_id=:user_id;", {"plant_id": plant_id, "user_id": user_id})
            existingQuantity = cursor.fetchall()

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


        # If there is already some plant in the basket
        if len(existingQuantity) > 0:


            # Sum the quantities
            newQuantity = int(existingQuantity[0][0]) + int(quantity)


            # Update table with new quantity
            try:

                sqliteConnection = sqlite3.connect("database.db")
                cursor = sqliteConnection.cursor()

                user_id = session["user_id"]
                subtotal = int(newQuantity) * int(price)
                
                # Update database with quantity
                cursor.execute("UPDATE baskets SET quantity=:quantity, subtotal=:subtotal WHERE plant_id=:plant_id AND user_id=:user_id", {"plant_id": plant_id, "user_id": user_id, "quantity": newQuantity, "subtotal": int(subtotal)})
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


        # First time the user has put this plant in the basket
        else:

            try:

                sqliteConnection = sqlite3.connect("database.db")
                cursor = sqliteConnection.cursor()
                user_id = session["user_id"]
                subtotal = int(quantity) * int(price)
                
                # Update database with quantity
                cursor.execute("INSERT INTO baskets(plant_id, user_id, quantity, name, picture, price, subtotal) VALUES (:plant_id, :user_id, :quantity, :name, :picture, :price, :subtotal)", {"plant_id": plant_id, "user_id": user_id, "quantity": quantity, "name": name, "picture": picture, "price": price, "subtotal": int(subtotal)})
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


        flash("Added to basket")
        return redirect("/")


    else:

        # Query database for plants to display them
        try:

            sqliteConnection = sqlite3.connect("database.db")
            cursor = sqliteConnection.cursor()

            # Set correct status for query
            status = "Yes"
            
            # Query database
            cursor.execute("SELECT * FROM plants WHERE show=:show;", {"show": status})
            plants = cursor.fetchall()

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

        return render_template("index.html", name=getUserName(), picture=getUserPicture(), role=getUserRole(), plants=plants)