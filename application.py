import os

from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from routes.profile import profile
from routes.message import message
from routes.index import index
from routes.signup import signup
from routes.logout import logout
from routes.login import login

# Configure application
app = Flask(__name__)

# Configure bluepprints
app.register_blueprint(login)
app.register_blueprint(signup)
app.register_blueprint(logout)
app.register_blueprint(index)
app.register_blueprint(profile)
app.register_blueprint(message)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
