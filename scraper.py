import asyncio  #import asynchronous execution
import time
import pymongo #allows connection to database
from pyppeteer import launch #used for website scraping
from datetime import datetime
from threading import Event

############# ENVIRONMENT VARIABLES ########################

DATABASE_NAME = "db"
DATABASE_PORT = 27017
DATABASE_HOST = "mongodb://localhost/"

DATABASE_USERNAME = "root"
DATABASE_PASSWORD = "example"

WEBSITES = ['https://cnn.com', 'https://foxnews.com']

POLL_INTERVAL = 15

############################################################

############# Try to connect to database ###################

try:
    myclient = pymongo.MongoClient( DATABASE_HOST, DATABASE_PORT, username = DATABASE_USERNAME, password = DATABASE_PASSWORD )
    print("[+] Database connected!")

except Exception as e:
    print("[+] Database connection error!")
    raise e

db_archive = myclient["archive"]
db_collection = db_archive["newsites"]

####################################################################

############### Scrape Website #######################################

async def capture(website):
        browser = await launch()
        page = await browser.newPage() #Create a new browser page
        await page.goto(website)
        element = await page.querySelector('h2')
        headline = await page.evaluate('(element) => element.textContent', element) 
        await browser.close() #close browser
        return(headline)

##################################################################################

##################### Handles database uploads ###################################

def data_upload():
    for  x in range(0, len(WEBSITES)):
        headline = asyncio.get_event_loop().run_until_complete(capture(WEBSITES[x]))
        site = WEBSITES[x].replace("https://","")
        site = site.replace(".com", "")
        site = site.upper()
        try:
            if (db_collection.find_one(skip=x)["Headline"] != headline):
                print("[+] Headline Update For" + " " + site)
                format_data = {"Site": site, "Headline": headline, "Date": datetime.now()}
                db_collection.insert_one(format_data)
            else:
                print("[+] No Headline Update For" + " " + site)
        except TypeError:
            print("[+] No Database Exists, Creating New Database")
            for  x in range(0, len(WEBSITES)):
                headline = asyncio.get_event_loop().run_until_complete(capture(WEBSITES[x]))         
                site = WEBSITES[x].replace("https://","")
                site = site.replace(".com", "")
                site = site.upper()
                format_data = {"Site": site, "Headline": headline, "Date": datetime.now()}
                db_collection.insert_one(format_data)
            break

def main():
    try:
        data_upload()
        print("\n")
        time.sleep(POLL_INTERVAL)
    except KeyboardInterrupt:
        print("[+] Exiting!")
        exit()

if __name__ == "__main__":
    main()







