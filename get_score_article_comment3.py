#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'simranjitsingh'

import csv
import mysql.connector
import time
import json
import requests
from calculate_score import calcPersonalXPScores, calBrevity, calcReadability, escape_string
from calculate_score_old import calRecommendationScore

cnx = mysql.connector.connect(user='merrillawsdb', password='WR3QZGVaoHqNXAF',
                              host='awsdbinstance.cz5m3w6kwml8.us-east-1.rds.amazonaws.com',
                              database='comment_iq')
cursor = cnx.cursor()

csvFile = open("AR_CR_withBody.csv", 'Ur')
csvReader = csv.reader(csvFile, delimiter=',', quotechar='"')

fileWriter = csv.writer(open("AR_CR_others.csv", "wb"),delimiter=",")

for row in csvReader:
    # if csvReader.line_num == 1:
    #     header = row
    #     print header
    #     header = ["userID","status","commentBody","approveDate","recommendationCount", \
    #                         "location","display_name","userComments","times_people", \
    #                         "commentSequence","editorsSelection","ArticleRelevance","ConversationalRelevance", \
    #                         "PersonalXP","Readability","Brevity","RecommendationScore","Latitude","Longitude"]
    #     # fileWriter.writerow(header)
    # else:

        commentBody = row[2]
        scores = [calcPersonalXPScores(commentBody),calcReadability(commentBody), \
                          calBrevity(commentBody),calRecommendationScore(row[4])]
        print scores
        data = row + scores
        fileWriter.writerow(data)
