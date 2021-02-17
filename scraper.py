#NOTE This code is hell and I don't want to comment it

import asyncio  #import asynchronous execution
import time
import pymongo #allows connection to database
import config
from pyppeteer import launch #used for website scraping
from datetime import datetime #used for timestamps
from threading import Event #multithreading support for api and scraper

############# ENVIRONMENT VARIABLES (Set in config.py file) ####################################

DATABASE_NAME = config.DATABASE_NAME
DATABASE_PORT = config.DATABASE_PORT
DATABASE_HOST = config.DATABASE_HOST

DATABASE_USERNAME = config.DATABASE_USERNAME
DATABASE_PASSWORD = config.DATABASE_PASSWORD

WEBSITES = config.WEBSITES

POLL_INTERVAL = config.POLL_INTERVAL

###############################################################################################

############### Scrape Website #################################################################

async def capture(website):
        browser = await launch(options={'args': ['--no-sandbox']})
        page = await browser.newPage() #Create a new browser page
        await page.goto(website)
        element = await page.querySelector('h2')
        headline = await page.evaluate('(element) => element.textContent', element) 
        await browser.close() #close browser
        return(headline)

###############################################################################################

##################### Handles database uploads ################################################

def check_existence(format_data):
    for x in range(0, db_collection.count_documents({})):
        if(db_collection.find_one(skip=x, sort=[( '_id', pymongo.DESCENDING )])["Site"] == format_data["Site"]):
            if(db_collection.find_one(skip=x, sort=[( '_id', pymongo.DESCENDING )])["Headline"] == format_data["Headline"]):
                return(True)
            else:
                return(False)
    print("outer")
    return(False)

def data_upload():
    print(db_collection.count_documents({}))
    for  x in range(0, len(WEBSITES)):
        headline = asyncio.get_event_loop().run_until_complete(capture(WEBSITES[x]))
        site = WEBSITES[x].replace("https://","")
        site = site.replace(".com", "")
        site = site.replace(".ca", "")
        site = site.upper()

        format_data = {"Site": site, "Headline": headline, "Date": datetime.now()}
        if (not check_existence(format_data)):
            print("[+] Headline Update For" + " " + site)
            db_collection.insert_one(format_data)
        else:
            print("[+] No Headline Update For" + " " + site)

#############################################################################################

def main(database):
    global db_collection
    db_collection = database

    while(True):
        try:
            data_upload()
            print("\n")
            time.sleep(POLL_INTERVAL)
        except KeyboardInterrupt:
            print("[+] Scraper Exiting!")
            exit()







