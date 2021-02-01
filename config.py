###############################################################################
#   Enter configuration contants in this file, This should only need          #
#   to be done once.                                                          #
#                                                                             #
#                                                                             #
#                                                                             #
###############################################################################

DATABASE_NAME = "db"
DATABASE_PORT = 27017
DATABASE_HOST = "mongodb://mongo/" #should be localhost if running locally if running in docker it should be mongo

DATABASE_USERNAME = "root" #The user of your mongo database
DATABASE_PASSWORD = "example" #The password of your mongo database, PLEASE CHANGE!!!

WEBSITES = ['https://cnn.com', 'https://foxnews.com'] #Set websites to archive; you can set as many as you want, seperated by a comma. 

POLL_INTERVAL = 300 #The length Of Time to wait before checking for a website update
