__author__ = 'simranjitsingh'

import mysql.connector
from ConfigParser import SafeConfigParser
import re
import csv

parserDb = SafeConfigParser()
# Edit the config file to fill in your credentials
parserDb.read('apidata/database.ini')

# Fetch the credentials from config file
user = parserDb.get('credentials', 'user')
password = parserDb.get('credentials', 'password')
host = parserDb.get('credentials', 'host')
database = parserDb.get('credentials', 'database')

header = ["UserID","Genders","DisplayName"]

fileWriter_only_name = csv.writer(open("apidata/only_name_change_1M.csv", "wb"),delimiter=",")
fileWriter_only_name.writerow(header)

fileWriter_gender_name = csv.writer(open("apidata/both_gender_name_change_1M.csv", "wb"),delimiter=",")
fileWriter_gender_name.writerow(header)

cnx = mysql.connector.connect(user=user, password=password, host=host, database=database)
cursor = cnx.cursor()


cursor.execute("SET net_read_timeout=360000")


cursor.execute("select userID,GROUP_CONCAT(DISTINCT(gender) SEPARATOR ' | ') "
               "as genders, GROUP_CONCAT(DISTINCT(display_name) SEPARATOR ' | ') as dsp_name "
               "from nyt_sample3  group by userID")
for i in cursor:
    s1 = re.findall(r'[|]',i[1])
    s2 = re.findall(r'[|]',i[2])
    if len(s2) > 0 and len(s1) == 0:
        print i
        try:
            fileWriter_only_name.writerow(i)
        except:
            continue
    if len(s2) > 0 and len(s1) > 0:
        print i
        try:
            fileWriter_gender_name.writerow(i)
        except:
            continue


