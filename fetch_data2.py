__author__ = 'ssachar'

# from ConfigParser import SafeConfigParser
#
# parserkeys = SafeConfigParser()
# # Edit the config file to fill in your api keys and values
# parserkeys.read('apidata/keys_config.ini')
#
# key_list =  parserkeys.options('API-KEYS')
#
# COMMUNITY_API_KEY_LIST = [parserkeys.get('API-KEYS', key) for key in key_list]
#
#
#
#
# COMMUNITY_API_KEY = parserkeys.get('API-KEYS', 'KEY1')
# COMMUNITY_API_KEY2 = parserkeys.get('API-KEYS', 'KEY2')
# COMMUNITY_API_KEY3 = parserkeys.get('API-KEYS', 'KEY3')
#
#
# COMMUNITY_API_KEY_LIST = [COMMUNITY_API_KEY,COMMUNITY_API_KEY2,COMMUNITY_API_KEY3]

import mysql.connector
from ConfigParser import SafeConfigParser
import time
import datetime

parser = SafeConfigParser()
parser.read('apidata/database.ini')

user = parser.get('credentials', 'user')
password = parser.get('credentials', 'password')
host = parser.get('credentials', 'host')
database = parser.get('credentials', 'database')

print "Current time " + time.strftime("%m/%d/%Y %I:%M:%S")

cnx = mysql.connector.connect(user=user, password=password,
                              host=host,
                              database=database)
cursor = cnx.cursor()

cursor.execute("select DATE_SUB(max(approveDate), INTERVAL 90 DAY) from vocab_comments ")
max_date = cursor.fetchall()[0][0].strftime("%Y-%m-%d")
print max_date
# for i in cursor:
#     print i[0].strftime("%m/%d/%Y %I:%M:%S")
#     print i[1].strftime("%m/%d/%Y %I:%M:%S")
#     a = i[0] + datetime.timedelta(days=-90)
#     print a.strftime("%m/%d/%Y %I:%M:%S")

# cursor.execute("select count(*) from vocab_comments where approveDate <= DATE_SUB(max(approveDate), INTERVAL 90 DAY)")
# cursor.execute("delete from vocab_comments where approveDate < (select DATE_SUB(max(approveDate), INTERVAL 90 DAY) from vocab_comments)")
# cursor.execute("delete from vocab_comments where approveDate < "
#                "(select commentID from "
#                "(select DATE_SUB(max(approveDate), INTERVAL 90 DAY) from vocab_comments)"
#                "as cid)")
# rowsaffected = cursor.rowcount
# print rowsaffected
#
cursor.execute("delete from vocab_comments where approveDate < '"+ max_date +"'")
rowsaffected = cursor.rowcount
print rowsaffected

# for i in cursor:
#     print i