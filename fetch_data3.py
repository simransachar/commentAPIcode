__author__ = 'ssachar'

import mysql.connector
import time
import json
import requests

# cnx = mysql.connector.connect(user='merrillawsdb', password='WR3QZGVaoHqNXAF',
#                              host='awsdbinstance.cz5m3w6kwml8.us-east-1.rds.amazonaws.com',
#                              database='comment_iq')

cnx = mysql.connector.connect(user='root', password='simran',
                              host='127.0.0.1',
                              database='comment_iq')


cursor = cnx.cursor()

def escape_string(string):
    res = string
    res = res.replace('\\','\\\\')
    res = res.replace('\n','\\n')
    res = res.replace('\r','\\r')
    res = res.replace('\047','\134\047') # single quotes
    res = res.replace('\042','\134\042') # double quotes
    res = res.replace('\032','\134\032') # for Win32
    return res

url_list = []
comment_id_list = []

cursor.execute("select articleURL,demo_articleID from articles")
data = cursor.fetchall()


for i in data:
    cursor.execute("select commentID from comments where articleURL = '"+ i[0] +"'")
    for j in cursor:
        list1 = [j[0],i[1]]
        comment_id_list.append(list1)
# for a in comment_id_list:
#       update_query = "UPDATE comments set demo_articleID = '"+ str(a[1]) +"' where commentID = '"+ str(a[0]) +"'"
#       cursor.execute(update_query)

for cid in comment_id_list:
    cursor.execute("select commentBody,approveDate,demo_articleID from comments where commentID = '"+ str(cid[0]) +"'")
    for j in cursor:
        current_time = j[1]
#        comment_text = escape_string(j[0])
        comment_text = j[0]
        demo_article_id = j[2]
        print demo_article_id
        url = "http://127.0.0.1:5000/get_scores"
        params = {'article_id' : demo_article_id, 'comment_text' : comment_text}
        param_json = json.dumps(params)
        response = requests.post(url, param_json)
        print response.json()
        ar_score = response.json()['ar_score']
        cr_score = response.json()['cr_score']
        demo_comment_id = response.json()['demo_comment_id']
        update = "UPDATE comments SET demo_commentID = '"+ str(demo_comment_id) +"' , ar_score = '"+ str(ar_score) +"'" \
                 ", cr_score = '"+ str(cr_score) +"' where commentID = '"+ str(cid[0]) +"'"
        cursor.execute(update)
#        cnx.commit()
cnx.close