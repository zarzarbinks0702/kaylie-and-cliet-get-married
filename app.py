from flask import Flask, render_template, jsonify, request, redirect
import sqlite3 as sql
import pandas as pd
import numpy as np
import os
import json

#init app and DB
app = Flask(__name__)

conn = sql.connect('static/wedding.db')

#############################################################
#############################################################
# Route to render index.html template
@app.route("/", methods=["POST"])
def home():
    return render_template("index.html")

@app.route("/rsvp", methods=["POST"])
def rsvp():
    return render_template("index.html")

@app.route("/travel", methods=["POST"])
def travel():
    return render_template("index.html")

@app.route("/schedule", methods=["POST"])
def schedule():
    return render_template("index.html")

@app.route("/registry", methods=["POST"])
def registry():
    return render_template("index.html")

#############################################################
conn.close()

@app.after_request
def add_header(r):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    r.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, public, max-age=0"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    return r

#main
if __name__ == "__main__":
    app.run(debug=True)
