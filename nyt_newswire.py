__author__ = 'simranjitsingh'

import pymysql
import csv


fileWriter = csv.writer(open("apidata/articleURLs.csv", "wb"),delimiter=",")

connection = pymysql.connect(user='merrillawsdb', passwd='WR3QZGVaoHqNXAF',
                                 host='awsdbinstance.cz5m3w6kwml8.us-east-1.rds.amazonaws.com',
                                 database='comment_iq')

cursor = connection.cursor()

query = ("select distinct(articleURL) from nyt_comments_all order by commentID desc")

cursor.execute(query)

for i in cursor:
    print i
    fileWriter.writerow(i)
