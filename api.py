import flask
import pymongo
import config
import isodate as iso
import json

from bson import ObjectId
from flask.json import JSONEncoder
from datetime import date

############# ENVIRONMENT VARIABLES (Set in config.py file) ####################################

###############################################################################################

############# Set database collection in main ######################################################
def main(database):

    global db_collection 
    db_collection = database
    

    ################################################################################################

    ################# JSON Encoder #################################################################

    class MongoJSONEncoder(JSONEncoder):
        def default(self, o):
            if isinstance(o, date):
                return iso.datetime_isoformat(o)
            if isinstance(o, ObjectId):
                return str(o)
            else:
                return super().default(o)

    ###############################################################################################

    app = flask.Flask(__name__)
    app.config["DEBUG"] = True


    @app.route('/', methods=['GET'])
    def home():
        return "<h1>Documentive Archive System</h1><p>This site is a prototype API for the documentive archive.</p>"

    # A route to return all of the available entries in the documentive archive
    @app.route('/api/v1/resources/entries/all', methods=['GET'])
    def api_all():
        return MongoJSONEncoder().encode(list(db_collection.find()))


    app.run(host="0.0.0.0")