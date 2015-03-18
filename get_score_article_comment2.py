#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'simranjitsingh'

import csv
import mysql.connector
import time
import json
import requests
from calculate_score_old import calRecommendationScore


cnx = mysql.connector.connect(user='merrillawsdb', password='WR3QZGVaoHqNXAF',
                              host='awsdbinstance.cz5m3w6kwml8.us-east-1.rds.amazonaws.com',
                              database='comment_iq')
cursor = cnx.cursor()

csvFile = open("article5_Data_work.csv", 'Ur')
csvReader = csv.reader(csvFile, delimiter=',', quotechar='"')

url = "http://127.0.0.1:5000/commentIQ/v1/addComment"

fileWriter = csv.writer(open("article5_Data_withScores.csv", "ab"),delimiter=",")

for row in csvReader:
    if csvReader.line_num == 1:
        header = row
        print header
        header = ["userID","status","commentBody","approveDate","recommendationCount", \
                            "location","display_name","userComments","times_people", \
                            "commentSequence","editorsSelection","ArticleRelevance","ConversationalRelevance", \
                            "PersonalXP","Readability","Brevity","RecommendationScore","Latitude","Longitude"]
        # fileWriter.writerow(header)
    else:
        commentBody = row[2]
        params = {'commentBody' : commentBody, 'articleID' : 129 }
        param_json = json.dumps(params)
        response = requests.post(url, param_json)
        r = response.json()
        print r
        scores = [r['ArticleRelevance'],r['ConversationalRelevance'],r['PersonalXP'],r['Readability'], \
                          r['Brevity'],calRecommendationScore(row[4])]
        data = row + scores
        fileWriter.writerow(data)

# file = open('articleText.txt', 'r')
# text = ""
# for line in file:
#     text = text + " " + line



# article_text = file.read()
# article_text = str(article_text)
# article_text = escape_string(article_text)
# article_text = text
# current_time = time.strftime("%Y-%m-%d %I:%M:%S")
#
# insert_query = "INSERT INTO articles (pubDate, full_text)" \
#                             " VALUES('%s', '%s')" % \
#                             (current_time, article_text)
# cursor.execute(insert_query)
# cnx.commit()
# articleID = cursor.lastrowid
# rowsaffected = cursor.rowcount
#
# print articleID
#
# cursor.execute("select full_text from articles where articleID = 123")
# for i in cursor:
#     print i[0]