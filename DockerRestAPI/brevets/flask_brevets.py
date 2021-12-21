"""
Replacement for RUSA ACP brevet time calculator
(see https://rusa.org/octime_acp.html)

Modified by: Abduarraheem Elfandi
To add database functionality for project 5.
"""

import os
import logging
import config
import flask
import json
import arrow  # Replacement for datetime, based on moment.js
import acp_times  # Brevet time calculations

from flask import request, redirect, url_for, render_template
from pymongo import MongoClient, errors
from bson.json_util import dumps

###
# Globals
###
app = flask.Flask(__name__)
CONFIG = config.configuration()
app.secret_key = CONFIG.SECRET_KEY

client = MongoClient('db', 27017)
db = client.acpbrevet

###
# Pages
###


@app.route("/")
@app.route("/index")
def index():
    app.logger.debug("Main page entry")
    return flask.render_template('calc.html')


@app.errorhandler(404)
def page_not_found(error):
    app.logger.debug("Page not found")
    flask.session['linkback'] = flask.url_for("index")
    return flask.render_template('404.html'), 404


###############
#
# AJAX request handlers
#   These return JSON, rather than rendering pages.
#
###############
@app.route("/_calc_times")
def _calc_times():
    """
    Calculates open/close times from miles, using rules
    described at https://rusa.org/octime_alg.html.
    Expects one URL-encoded argument, the number of miles.
    """
    app.logger.debug("Got a JSON request")
    km = request.args.get('km', 999, type=float)
    brevet_dist_km = request.args.get('brevet_dist_km', type=int) # get the brevet selected by the user.
    begin_date = request.args.get('begin_date', type=str) # date set by the user.
    begin_time = request.args.get('begin_time', type=str) # time set by the user.
    date_time = arrow.get(begin_date+ " " + begin_time + "-08:00").isoformat()

    app.logger.debug("km={}".format(km))
    app.logger.debug("request.args: {}".format(request.args))

    open_time = acp_times.open_time(km, brevet_dist_km, date_time)
    close_time = acp_times.close_time(km, brevet_dist_km, date_time)
    result = {"open": open_time, "close": close_time}
    return flask.jsonify(result=result)
#############

@app.route('/display')
def display():
    return flask.render_template('display.html')

@app.route('/send', methods=['POST'])
def send_to_db():
    brevets = json.loads(request.form["brevets"]) # get the ACP brevet time table
    # app.logger.debug("Got table data.")
    data = [] # will contain brevets that have open and close time.
    for row in brevets["controls"]:
        if row["close"] == "" and row["open"] == "":
            continue
        data.append(row)
    brevets["controls"] = data
    try:
        # app.logger.debug(brevets)
        db.acptable.insert_one(brevets) # insert the table entry.
    except:
        app.logger.debug("Failed to insert to the data base.")
    # app.logger.debug("Table data stored to db.")
    return redirect(url_for('index'))

@app.route('/_get_from_db')
def _get_from_db():
    # app.logger.debug("Requesting display...")
    if db.acptable.count() == 0:
        return flask.jsonify(result=[])
    data = list(db.acptable.find({}, {"_id": False})) # get the data from the db, filtered from the id and turn it into a list.
    # app.logger.debug("End of request.")
    return flask.jsonify(result=data)


app.debug = CONFIG.DEBUG
if app.debug:
    app.logger.setLevel(logging.DEBUG)

if __name__ == "__main__":
    print("Opening for global access on port {}".format(CONFIG.PORT))
    app.run(port=CONFIG.PORT, host="0.0.0.0")
