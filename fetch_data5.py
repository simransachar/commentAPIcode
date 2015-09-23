__author__ = 'simranjitsingh'

import mysql.connector

cnx = mysql.connector.connect(user='merrillawsdb', password='WR3QZGVaoHqNXAF',
                             host='awsdbinstance.cz5m3w6kwml8.us-east-1.rds.amazonaws.com',
                             database='comment_iq')

cursor = cnx.cursor()

cursor.execute("select commentiq_articleID,commentBody from client_comments where commentiq_articleID is not null and " \
               "commentiq_commentID is null order by approveDate")
for i in cursor:
    print i