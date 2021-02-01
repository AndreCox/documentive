import flask
import pymongo
import config
import isodate as iso
import json

from bson import ObjectId
from flask.json import JSONEncoder
from datetime import date

############# ENVIRONMENT VARIABLES (Set in config.py file) ####################################

DATABASE_NAME = config.DATABASE_NAME
DATABASE_PORT = config.DATABASE_PORT
DATABASE_HOST = config.DATABASE_HOST

DATABASE_USERNAME = config.DATABASE_USERNAME
DATABASE_PASSWORD = config.DATABASE_PASSWORD

WEBSITES = config.WEBSITES

POLL_INTERVAL = config.POLL_INTERVAL

###############################################################################################

############# Try to connect to database ######################################################
def main():
    try:
        myclient = pymongo.MongoClient( DATABASE_HOST, DATABASE_PORT, username = DATABASE_USERNAME, password = DATABASE_PASSWORD )
        print("[+] API Database connected!")

    except Exception as e:
        print("[+] API Database connection error!")
        raise e

    db_archive = myclient["archive"]
    db_collection = db_archive["newsites"]

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