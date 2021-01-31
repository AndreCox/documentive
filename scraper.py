import asyncio  #import asynchronous execution
import time
import pymongo #allows connection to database
from pyppeteer import launch #used for website scraping
from datetime import datetime
from threading import Event

############# ENVIRONMENT VARIABLES ###########################################################

DATABASE_NAME = "db"
DATABASE_PORT = 27017
DATABASE_HOST = "mongodb://mongot/" #should be localhost if running localy if running in docker it should be mongo

DATABASE_USERNAME = "root"
DATABASE_PASSWORD = "example"

WEBSITES = ['https://cnn.com', 'https://foxnews.com']

POLL_INTERVAL = 5 * 60

###############################################################################################

############# Try to connect to database ######################################################

try:
    myclient = pymongo.MongoClient( DATABASE_HOST, DATABASE_PORT, username = DATABASE_USERNAME, password = DATABASE_PASSWORD )
    print("[+] Database connected!")

except Exception as e:
    print("[+] Database connection error!")
    raise e

db_archive = myclient["archive"]
db_collection = db_archive["newsites"]

################################################################################################

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

def main():
    while(True):
        try:
            data_upload()
            print("\n")
            time.sleep(POLL_INTERVAL)
        except KeyboardInterrupt:
            print("[+] Exiting!")
            exit()

if __name__ == "__main__":
    main()







