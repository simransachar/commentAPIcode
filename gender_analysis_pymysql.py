__author__ = 'simranjitsingh'

import pymysql
import re
import csv

header = ["UserID","Genders","FirstName"]

fileWriter_only_name = csv.writer(open("apidata/only_FirstName_change_1M.csv", "wb"),delimiter=",")
fileWriter_only_name.writerow(header)

fileWriter_gender_name = csv.writer(open("apidata/both_Gender_FirstName_change_1M.csv", "wb"),delimiter=",")
fileWriter_gender_name.writerow(header)


connection = pymysql.connect(user='merrillawsdb', passwd='WR3QZGVaoHqNXAF',
                                 host='awsdbinstance.cz5m3w6kwml8.us-east-1.rds.amazonaws.com',
                                 database='comment_iq')

cursor = connection.cursor()

query = ("select userID,GROUP_CONCAT(DISTINCT(gender) SEPARATOR ' | ') "
               "as genders, GROUP_CONCAT(DISTINCT(userFirstName) SEPARATOR ' | ') as dsp_name "
               "from nyt_sample3  group by userID")

cursor.execute(query)

for i in cursor:
    print i
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
