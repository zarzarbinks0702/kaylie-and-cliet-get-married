from flask import Flask, render_template, jsonify, request, redirect
import sqlite3 as sql
import pandas as pd
import numpy as np
import os
import json

#init app and DB
app = Flask(__name__)

app.config['RSVP-KEYS'] = ['ButlerWedding1', 'ButerWedding2']

#############################################################
#############################################################
# Route to render index.html template
@app.route("/", methods=["GET", "POST"])
def home():
    return render_template("index.html")

@app.route("/rsvp", methods=["GET", "POST"])
def rsvp():
    return render_template("rsvp.html")

@app.route("/travel", methods=["GET", "POST"])
def travel():
    return render_template("travel.html")

@app.route("/schedule", methods=["GET", "POST"])
def schedule():
    return render_template("schedule.html")

@app.route("/registry", methods=["GET", "POST"])
def registry():
    return render_template("registry.html")
@app.route("/rsvpConfirm", methods=["GET", "POST"])
def rsvp_confirm():
    if request.method == "POST":
        rsvp_key = request.values["key"]
        if rsvp_key in app.config['RSVP-KEYS']:
            name = request.values["name"]
            rsvp = request.values["rsvp"]
            plus_one = request.values["plus-one"]
            guest = (name, rsvp, plus_one)
            conn = sql.connect('static/wedding.db')
            cursor = conn.cursor()
            insert = '''INSERT INTO guest_list(Name, RSVP, 'Plus One')
            VALUES (?,?,?)'''
            cursor.execute(insert, guest)
            conn.close()
            message = "RSVP confirmed. We can't wait to celebrate with you!"
        else:
            message = "RSVP failed. Please confirm your RSVP Key is correct and try again later."
    return render_template("success.html", message=message)
#############################################################

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
