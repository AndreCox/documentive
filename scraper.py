import asyncio  #import asynchronous execution
import pymongo
from pyppeteer import launch


async def capture(website, imgname):
    browser = await launch()
    page = await browser.newPage() #Create a new browser page
    await page.goto(website)
    element = await page.querySelector('h2')
    headline = await page.evaluate('(element) => element.textContent', element) 
    await browser.close() #close browser
    print(headline)
    return(headline)


def main():
    asyncio.get_event_loop().run_until_complete(capture('https://cnn.com', 'cnn.png'))
    asyncio.get_event_loop().run_until_complete(capture('https://foxnews.com', 'fox.png'))

  

main()