from scraper import main as scraper_main
from api import main as api_main

from subprocess import call

from multiprocessing import Process

def api():
    print("[+] Starting Scraper!")
    scraper_main()
    #call(["python", "scraper.py"])

def scraper():
    print("[+] Starting API!")
    api_main()
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