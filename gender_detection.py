__author__ = 'simranjitsingh'

import sexmachine.detector as gender
from ConfigParser import SafeConfigParser
import mysql.connector
import re

# Get the config file for database
parserDb = SafeConfigParser()
# Edit the config file to fill in your credentials
parserDb.read('apidata/database.ini')

# Fetch the credentials from config file
user = parserDb.get('credentials', 'user')
password = parserDb.get('credentials', 'password')
host = parserDb.get('credentials', 'host')
database = parserDb.get('credentials', 'database')

cnx = mysql.connector.connect(user=user, password=password, host=host, database=database)
cursor = cnx.cursor()
# cursor.execute("SET net_read_timeout=36000")

# d = gender.Detector(case_sensitive=False)
name = "P.S. Ruckman, Jr."
s = re.findall(r'[aA-zZ]+',name)

if len(s) == 0:
    print "00"
else:
    print s[0]
# gender = d.get_gender(s[0])
#
# print gender
# def update_table(disp_name):
#     gender = d.get_gender(disp_name[0])
#     cursor.execute("update user_comments set gender = '" + gender + "' where commentID = '"+ str(disp_name[1]) +"'")
#     cnx.commit()
# list1=[]
# counter = 0
# cursor.execute("select display_name,commentID from user_comments where gender is null limit 20000")
# for val in cursor:
#     print val
#     list1.append(val)
# #list1 = cursor.fetchall()
# for disp_name in list1:
#
#     print disp_name[0] + ', Gender: ' + d.get_gender(disp_name[0])
#     update_table(disp_name)
#     counter = counter + 1
#     print counter