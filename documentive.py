import pymongo
import config

from scraper import main as scraper_main
from api import main as api_main
from subprocess import call
from multiprocessing import Process

############# ENVIRONMENT VARIABLES (Set in config.py file) ####################################

DATABASE_NAME = config.DATABASE_NAME
DATABASE_PORT = config.DATABASE_PORT
DATABASE_HOST = config.DATABASE_HOST

DATABASE_USERNAME = config.DATABASE_USERNAME
DATABASE_PASSWORD = config.DATABASE_PASSWORD

WEBSITES = config.WEBSITES

POLL_INTERVAL = config.POLL_INTERVAL

###############################################################################################


    

try:
    myclient = pymongo.MongoClient( DATABASE_HOST, DATABASE_PORT, username = DATABASE_USERNAME, password = DATABASE_PASSWORD )
    db_archive = myclient["archive"]
    global db_collection
    db_collection = db_archive["newsites"]
    print("[+] Database connected!")
except Exception as e:
    print("[+] Database connection error!")
    raise e

def api():
    print("[+] Starting Scraper!")
    scraper_main(db_collection)
    #call(["python", "scraper.py"])

def scraper():
    print("[+] Starting API!")
    api_main(db_collection)
    #call(["python", "scraper.py"])

def main():
    while(True):
        try:
            scraper_process = Process(target=scraper)
            scraper_process.start()
            api_process = Process(target=api)
            api_process.start()
            scraper_process.join()
            api_process.join()

        except KeyboardInterrupt:
            print("[+] Exiting!")
            exit()

if __name__ == "__main__":
    main()