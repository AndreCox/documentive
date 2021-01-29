import asyncio  #import asynchronous execution
import pymongo
import time, threading

from pyppeteer import launch

from datetime import timedelta #Used by timeloop to get the time

async def capture(website):
    while(True):
        browser = await launch()
        page = await browser.newPage() #Create a new browser page
        await page.goto(website)
        element = await page.querySelector('h2')
        headline = await page.evaluate('(element) => element.textContent', element) 
        await browser.close() #close browser
        print(headline)
        await asyncio.sleep(15)

def periodic_capture():
    asyncio.get_event_loop().run_until_complete(capture('https://cnn.com'))
    asyncio.get_event_loop().run_until_complete(capture('https://foxnews.com'))


if __name__ == "__main__":
    periodic_capture()
