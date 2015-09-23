__author__ = 'simranjitsingh'

import mysql.connector
import time
import json
import requests

cnx = mysql.connector.connect(user='merrillawsdb', password='WR3QZGVaoHqNXAF',
                             host='awsdbinstance.cz5m3w6kwml8.us-east-1.rds.amazonaws.com',
                             database='comment_iq')

cursor = cnx.cursor()

base_url = "http://api.comment-iq.com/commentIQ/v1"
url = base_url + "/updateComment"

list1 = []
cursor.execute("select commentiq_commentID,commentBody from client_comments where commentiq_commentID is not null " \
               " and commentLength is null order by rand()")
for data in cursor:
    list1.append(data)
# list1 = cursor.fetchall()
cnx.close

for i in list1:
    print i[0]
    params = {'commentBody' : i[1], 'commentID' : i[0] }
    param_json = json.dumps(params)
    response = requests.post(url, param_json)
    print response.json()