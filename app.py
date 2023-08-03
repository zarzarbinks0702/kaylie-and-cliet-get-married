from flask import Flask, render_template, jsonify, request, redirect
import psycopg2 as sql
import pandas as pd
import numpy as np
import os
import json

#init app and DB
app = Flask(__name__)

app.config['RSVP-KEYS'] = ['BUTLERRECEPTION48593', 'BUTLERRECEPTION19852']

app.config['RSVP-KEYS-BACHELORETTE'] = ['BUTLERRECEPTION92494',
'BUTLERRECEPTION61566',
'BUTLERRECEPTION66428',
'BUTLERRECEPTION51638',
'BUTLERRECEPTION98924',
'BUTLERRECEPTION40638',
'BUTLERRECEPTION51065']

app.config['RSVP-KEYS-PLUS-ONES'] = ['BUTLERRECEPTION95662',
'BUTLERRECEPTION63633',
'BUTLERRECEPTION57989',
'BUTLERRECEPTION39017',
'BUTLERRECEPTION77868',
'BUTLERRECEPTION40750',
'BUTLERRECEPTION89221',
'BUTLERRECEPTION58429',
'BUTLERRECEPTION16122',
'BUTLERRECEPTION27425',
'BUTLERRECEPTION94260',
'BUTLERRECEPTION96462',
'BUTLERRECEPTION77450',
'BUTLERRECEPTION78386',
'BUTLERRECEPTION33081',
'BUTLERRECEPTION40780']

app.config['RSVP-KEYS-CEREMONY-MEAL'] = ['BUTLERRECEPTION86474',
'BUTLERRECEPTION41272',
'BUTLERRECEPTION56758',
'BUTLERRECEPTION91305',
'BUTLERRECEPTION44981',
'BUTLERRECEPTION86544']

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

@app.route("/rsvpContinue1", methods=["GET", "POST"])
def rsvpContinue1():
    if request.method == "POST":
        rsvp_key = request.form.get("key")
        if rsvp_key in app.config['RSVP-KEYS-PLUS-ONES']:
            return render_template("rsvpformplusones.html")
        elif rsvp_key in app.config['RSVP-KEYS-BACHELORETTE']:
            return render_template("rsvpformbachelorette.html")
        elif rsvp_key in app.config['RSVP-KEYS']:
            return render_template("rsvpform.html")
        elif rsvp_key in app.config['RSVP-KEYS-CEREMONY-MEAL']:
            return render_template("rsvpformceremony.html")
        else:
            message = "RSVP failed. Please confirm your RSVP Key is correct and try again later."
            return render_template("success.html", message=message)

@app.route("/rsvpConfirm", methods=["GET", "POST"])
def rsvp_confirm():
    if request.method == "POST":
        name = request.form.get("name")
        rsvp = request.form.get("rsvp")
        food = request.form.get("food-choice")
        cheese_1 = request.form.get("cheese1")
        try: plus_one = request.form.get("plus-one")
        except: plus_one = "None"
        try: plus_one_food = request.form.get("plus-one-food")
        except: plus_one_food = "None"
        try: cheese_2 = request.form.get("cheese2")
        except: cheese_2 = "None"
        try: bachelorette = request.form.get("bachelorette")
        except: bachelorette = "None"
        try: ceremony_meal = request.form.get("ceremony-meal")
        except: ceremony_meal = "None"
        note = request.form.get("notes")
        pw = os.environ.get('pw')
        user = os.environ.get('user')
        host = os.environ.get('host')
        db = os.environ.get('db')
        conn = sql.connect(database=db,
                    user=user,
                    password=pw,
                    host=host, port="5432")
        cursor = conn.cursor()
        insert = """INSERT INTO guest_list(Name, RSVP, Food_Choice, Cheese_1, Plus_One, Plus_One_Food, Cheese_2, Bachelorette, Ceremony_Meal, Notes) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
        cursor.execute(insert, (name, rsvp, food, cheese_1, plus_one, plus_one_food, cheese_2, bachelorette, ceremony_meal, note))
        conn.commit()
        cursor.close()
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
