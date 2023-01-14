from flask import Flask, render_template, jsonify, request, redirect
import psycopg2 as sql
import pandas as pd
import numpy as np
import os
import json
from config.py import config

#init app and DB
app = Flask(__name__)

app.config['RSVP-KEYS'] = ['ButlerReception86474',
'ButlerReception41272',
'ButlerReception95662',
'ButlerReception63633',
'ButlerReception57989',
'ButlerReception48593',
'ButlerReception92494',
'ButlerReception61566',
'ButlerReception39017',
'ButlerReception66428',
'ButlerReception77868',
'ButlerReception51638',
'ButlerReception40750',
'ButlerReception98924',
'ButlerReception40638',
'ButlerReception89221',
'ButlerReception58429',
'ButlerReception56758',
'ButlerReception91305',
'ButlerReception16122',
'ButlerReception44981',
'ButlerReception22639',
'ButlerReception27425',
'ButlerReception94260',
'ButlerReception96462',
'ButlerReception77450',
'ButlerReception78386',
'ButlerReception33081',
'ButlerReception51065',
'ButlerReception40780']

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
        rsvp_key = request.form.get("key")
        if rsvp_key in app.config['RSVP-KEYS']:
            name = request.form.get("name")
            rsvp = request.form.get("rsvp")
            plus_one = request.form.get("plus-one")
            food = request.form.get("food-choice")
            plus_one_food = request.form.get("plus-one-food")
            note = request.form.get("notes")
            guest = (name, rsvp, food, plus_one, plus_one_food, note)
            params = config()
            conn = sql.connect(**params)
            cursor = conn.cursor()
            insert = 'INSERT INTO guest_list(Name, RSVP, Food_Choice, Plus_One, Plus_One_Food, Notes) VALUES (?,?,?,?,?)'
            cursor.execute(insert, guest)
            conn.commit()
            conn.close()
            app.config['RSVP-KEYS'].remove(rsvp_key)
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
