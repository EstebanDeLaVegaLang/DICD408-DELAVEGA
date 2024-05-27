import sqlalchemy 
import pandas as pd
from sqlalchemy_orm import session
import requests
import json
from datetime import datetime
import datetime
import sqlite3

Database_location = ""
User_ID = ""
Token = ""

headers = {
    "Accept" : "application/)son",
    "Content-Type" : "application/json", 
    "Authorization" : "Bearer {oken}".format(token = Token)
}

today = datetime.datetime.now()
yesterday = today - datetime.timedelta(days = 1) 
yesterday_unix_timestamp = int(yesterday.timestamp()) * 1000

r = requests.get("")