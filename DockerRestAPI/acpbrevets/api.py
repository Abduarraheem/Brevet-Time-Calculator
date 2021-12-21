# ACP brevet Service
"""
Author: Abduarraheem Elfandi
Project 6: Rest API
CIS 322
"""

import os
import io
import logging
import json
from flask import Flask, send_file
from flask_restful import Resource, Api, reqparse
from pymongo import MongoClient
import pandas



# Instantiate the app
app = Flask(__name__)
api = Api(app)
client = MongoClient('db', 27017)
db = client.acpbrevet

class ListAll(Resource):
    """
    Get all the data from the database in json format.
    """
    def get(self):
        if db.acptable.count() == 0:
            return {'brevets':[]}
        brevets = list(db.acptable.find({}, {'_id': False})) # get the brevets from the db, filtered from the id and turn it into a list.
        data = {'brevets': brevets}
        return data

def getBrevets(top, time_type):
    """
    Returns brevets from the database depending on the request.
    """
    # check what we need to exclude and what we need to include for
    # the open and close times.

    if time_type == "open":
        exclude_time = "controls.close"
    else:
        exclude_time = "controls.open"
    include_time = "controls." + time_type
    
    if db.acptable.count() == 0 or top == 0: # if there is nothing in the database or top 0 was requested just return empty list
        return []

    if not top: # if top k was not requested then display everything in the data base.
        brevets = list(db.acptable.find({}, {'_id': False,  exclude_time: False}))
    else:
        # sort based on time_type and filter out depending on the time_type
        brevets = list(db.acptable.aggregate([{"$project": 
            {'_id':False, 'distance': True, 'begin_date': True, 'begin_time': True, include_time: True, 
            'controls.miles': True, 'controls.km': True, 'controls.location': True }}, 
            {"$unwind": "$controls"}, {"$sort":{include_time: 1}},{"$limit":top}]))
        for brevet in brevets: # aggregate changes the controls to dict instead of a list of dicts, so this needs to be done.
              brevet['controls'] = [brevet['controls']]
    return brevets

def toCSV(brevets):
        """
        Function that will turn the brevets gotten from the database to csv stream format.
        Input: List of brevets
        Output: a string stream of the csv.
        """
        csv_f = pandas.json_normalize(brevets, record_path=['controls'], meta=['begin_time', 'begin_date','distance']) # turn data into csv format.
        csv_f.to_csv("data.csv", index=False) # store the data to the stream in csv format
        return send_file("data.csv", mimetype='text/csv') # return the string stream of the csv.

class listAllcsv(Resource):
    """
    Get all the data from the database in csv format.
    """
    def get(self):
        if db.acptable.count() == 0:
            brevets = []
            return toCSV(brevets)
        brevets = list(db.acptable.find({}, {'_id': False})) # get the brevets from the db, filtered from the id and turn it into a list.
        return toCSV(brevets)


class ListOpenOnly(Resource):
    """
    Get the open time data from the database in json format.
    """
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('top', type=int, required=False, location='args')
        arg = parser.parse_args()
        top = arg['top']
        brevets = getBrevets(top, "open")
        data = {'brevets': brevets}
        return data

class listOpenOnlycsv(Resource):
    """
    Get the open time data from the database in csv format.
    """
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('top', type=int, required=False, location='args')
        arg = parser.parse_args()
        top = arg['top']

        brevets = getBrevets(top, "open")
        return toCSV(brevets)


class ListCloseOnly(Resource):
    """
    Get the close time data from the database in json format.
    """
    def get(self):
        if db.acptable.count() == 0:
            return {'brevets':[]}
        parser = reqparse.RequestParser()
        parser.add_argument('top', type=int, required=False, location='args')
        arg = parser.parse_args()
        top = arg['top']

        brevets = getBrevets(top, "close")
        data = {'brevets':brevets}
        return data

class listCloseOnlycsv(Resource):
    """
    Get the close time data from the database in csv format.
    """
    def get(self):
        if db.acptable.count() == 0:
            brevets = []
            return toCSV(brevets)
        parser = reqparse.RequestParser()
        parser.add_argument('top', type=int, required=False, location='args')
        arg = parser.parse_args()
        top = arg['top']

        brevets = getBrevets(top, "close")
        return toCSV(brevets)

# Create routes
# Another way, without decorators
api.add_resource(ListAll,'/', '/listAll', '/listAll/json')
api.add_resource(listAllcsv, '/listAll/csv') 

api.add_resource(ListOpenOnly, '/listOpenOnly', '/listOpenOnly/json')
api.add_resource(listOpenOnlycsv,'/listOpenOnly/csv')

api.add_resource(ListCloseOnly, '/listCloseOnly', '/listCloseOnly/json')
api.add_resource(listCloseOnlycsv, '/listCloseOnly/csv')

# Run the application
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
