__author__ = 'simranjitsingh'

import csv
import mysql.connector
import time
import datetime
from calculate_score import calBrevity, calcReadability, calcPersonalXPScores, escape_string

cnx = mysql.connector.connect(user='merrillawsdb', password='WR3QZGVaoHqNXAF',
                              host='awsdbinstance.cz5m3w6kwml8.us-east-1.rds.amazonaws.com',
                              database='comment_iq')
cursor = cnx.cursor()

csvFile = open("new_unique_userIDs_picked_comments_work.csv", 'Ur')
csvReader = csv.reader(csvFile, delimiter=',', quotechar='"')

userIDlist = []
for row in csvReader:
    userIDlist.append(row[0])
fileWriter = csv.writer(open("picked_userscores_deok.csv", "ab"),delimiter=",")
header = ["userID","AVGPersonalXP","AVGReadability","AVGBrevity","AVGRecommendationScore","AVGPicks","AVGcommentspermonth"]
# fileWriter.writerow(header)

for u_id in userIDlist:

    brevity_list = []
    personalXP_list = []
    readability_list = []
    approvedate_list = []
    sum1 = 0
    sum2 = 0
    sum3 = 0
    sum4 = 0
    sumread = 0
    cursor.execute("select commentBody,recommendationCount,editorsSelection,approveDate" \
                   "  from user_comments where user_id = '"+u_id+"' order by approveDate")
    for i in cursor:
        brevity = calBrevity(i[0])
        brevity_list.append(brevity)
        personalXP = calcPersonalXPScores(i[0])
        personalXP_list.append(personalXP)
        readability = calcReadability(i[0])
        readability_list.append(readability)
        approvedate = i[3]
        approvedate_list.append(approvedate)
        sum1 = sum1 + brevity
        sum2 = sum2 + personalXP
        sum3 = sum3 + i[1]
        sum4 = sum4 + i[2]
        sumread = sumread + readability

    dd =  approvedate_list[-1] - approvedate_list[0]
    daycount = dd.days
    print daycount
    months =  float(daycount) / float(30)

    # months =  int(daycount) / 30
    if months < 1:
        # comment_month = 0
        comment_month = len(readability_list)
    else:
        comment_month = float(len(readability_list))/ float(months)
    print comment_month
    a = float(sum1)/float(len(brevity_list))
    b = float(sum2)/float(len(personalXP_list))
    c = float(sum3)/float(len(personalXP_list))
    d = float(sum4)/float(len(personalXP_list))
    e = float(sumread)/float(len(personalXP_list))

    # header = ["userID","AVGPersonalXP","AVGReadability","AVGBrevity","AVGRecommendationScore","AVGPicks","AVGcommentspermonth"]
    # fileWriter.writerow(header)
    data = [u_id,b,e,a,c,d,comment_month]
    print data
    fileWriter.writerow(data)
