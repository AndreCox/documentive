import asyncio  #import asynchronous execution
import time, threading
import pymongo #allows connection to database
from pyppeteer import launch #used for website scraping
from datetime import datetime

#############ENVIRONMENT VARIABLES########################

DATABASE_NAME = "db"
DATABASE_PORT = 27017
DATABASE_HOST = "mongodb://localhost/"

DATABASE_USERNAME = "root"
DATABASE_PASSWORD = "example"

##########################################################

#############Try to connect to database###################

try:
    myclient = pymongo.MongoClient( DATABASE_HOST, DATABASE_PORT, username = DATABASE_USERNAME, password = DATABASE_PASSWORD )
    print("[+] Database connected!")

except Exception as e:
    print("[+] Database connection error!")
    raise e

db_archive = myclient["archive"]
db_collection = db_archive["newsites"]

async def capture(website):
        browser = await launch()
        page = await browser.newPage() #Create a new browser page
        await page.goto(website)
        element = await page.querySelector('h2')
        headline = await page.evaluate('(element) => element.textContent', element) 
        await browser.close() #close browser
        print("[+] " + headline)
        return(headline)

def periodic_capture():
    cnn = asyncio.get_event_loop().run_until_complete(capture('https://cnn.com'))
    fox = asyncio.get_event_loop().run_until_complete(capture('https://foxnews.com'))
    
    store_cnn = {"Site": "CNN", "Headline": cnn, "Date": datetime.now()}
    store_fox = {"Site": "FOX", "Headline": fox, "Date": datetime.now()}
    
    x = db_collection.insert_one(store_cnn)
    x = db_collection.insert_one(store_fox)

    time.sleep(15)
    periodic_capture()

if __name__ == "__main__":
    periodic_capture()




