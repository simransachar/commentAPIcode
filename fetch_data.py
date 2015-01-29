# -*- coding: utf-8 -*-
__author__ = 'simranjitsingh'

import csv
import mysql.connector
import time
import json
import timeit

print "Current time " + time.strftime("%m/%d/%Y %I:%M:%S")

cnx = mysql.connector.connect(user='root', password='simran',
                              host='127.0.0.1',
                              database='comment_iq')


# cnx = mysql.connector.connect(user='merrillawsdb', password='WR3QZGVaoHqNXAF',
#                              host='awsdbinstance.cz5m3w6kwml8.us-east-1.rds.amazonaws.com',
#                              database='comment_iq')
cursor = cnx.cursor()
#cursor.execute("select * from city")
#cursor.execute("ALTER TABLE comments ADD cr_score TEXT AFTER ar_score")
#cursor.execute("ALTER TABLE comments CHANGE score ar_score TEXT")
#cursor.execute("drop table comments")
#cnx.commit()
#cursor.execute("delete from comments")
#cursor.execute("DESCRIBE demo_comments")
#cursor.execute("DESCRIBE comments")
# data = []
# cursor.execute("select * from comments limit 100")
# for i in cursor:
#     data.append(i)
#data = cursor.fetchall()
#cursor.execute("select commentID from demo_comments limit 10")
#cursor.execute("select count(*) from comments")
# start = timeit.default_timer()
# #cursor.execute("select count(*) from comments")
# cursor.execute("select * from comments order by commentID desc limit 5")
# stop = timeit.default_timer()
# print stop - start
# s1 = "Kalinda is a wonderful and wholly original creation of Ms. Panjabi and the show's writers and, as a heterosexual male, I'm always happy to watch her doing the nasty with guys and gals alike. Even so, it has to be said that a double standard continues to exist on television (both commercial and cable) for portrayals of gay and lesbian sex. It seems as though TV's creative minds can be as risque as they want to be when presenting hot sex between women - especially young women who look more like fashion-models than legal researchers or CIA employees. Gay men, on the other hand, are still pretty much restricted to chaste kisses, flirtatious glances and rather lame come-ons. If we've finally matured sufficiently as a nation to accept the reality of gay sex (or as much of it as can be presented without actually having anyone take their clothers off!) why do we still pretend that gay men don't have as much fun as gay women do? "
# res = s1
# res = res.replace('\\','\\\\')
# res = res.replace('\n','\\n')
# res = res.replace('\r','\\r')
# res = res.replace('\047','\134\047') # single quotes
# res = res.replace('\042','\134\042') # double quotes
# res = res.replace('\032','\134\032') # for Win32
# s1 = res
# cursor.execute("INSERT INTO comments (status, commentSequence, commentBody, approveDate,"
#                " recommendationCount, editorsSelection, display_name, location, articleURL)"
#                " VALUES('approved', 13102508,'"+s1+"'"
#                ", FROM_UNIXTIME(1413777606), 2, 0, 'stu freeman', '', "
#                "'http://artsbeat.blogs.nytimes.com/2014/10/19/the-good-wife-recap-alicia-turns-the-tables-on-peter/')")
# csvFile = open("data/articles2.csv", 'Ur')
# csvReader = csv.reader(csvFile, delimiter=',', quotechar='"')
# for row in csvReader:
    # if csvReader.line_num > 1:



# cnx.close()

# cnx = mysql.connector.connect(user='root', password='simran',
#                               host='127.0.0.1',
#                               database='comment_iq')
# cursor = cnx.cursor()

# cursor.execute("DESCRIBE articles")
# for i in cursor:
#     print i
# for row in data:
#         # insert_query = "INSERT INTO articles (pubDate, headline, full_text, materialType, snippet)" \
#         #                            " VALUES('%s', '%s', '%s', '%s', '%s', '%s')" % \
#         #                            (row[1], row[2], row[5],row[4],row[5])
#         # insert_query = "INSERT INTO comments (pubDate, headline,  full_text, materialType," \
#         #                            " articleURL)" \
#         #                            " VALUES('%s','%s', '%s', '%s', '%s')" % \
#         #                            (row[1], row[2] ,row[6] , row[4] , row[3])
#         # insert_query = "INSERT INTO comments (status, commentSequence, commentBody," \
#         #                            " approveDate, recommendationCount, editorsSelection, display_name," \
#         #                            " location, articleURL)" \
#         #                            " VALUES('%s', %d, '%s', '%s', %d, %d, '%s', '%s', '%s')" % \
#         #                            (row[9], row[8], row[2], row[3],row[4] , row[11] , row[5] , row[6] ,row [10])
#         insert_query = "INSERT INTO comments (status, commentSequence, " \
#                                    " approveDate, recommendationCount, editorsSelection, display_name," \
#                                    " location, articleURL)" \
#                                    " VALUES('%s', %s, '%s', '%s', %s, %s, '%s', '%s', '%s')" % \
#                                    (row[9], row[8], row[3],row[4] , row[11] , row[5] , row[6] ,row [10])
#
# #        print insert_query
#         cursor.execute(insert_query)
# #cnx.commit()

#cursor.execute("select * from demo_comments limit 10")
commentID = 6734
# cursor.execute("select articleID from demo_comments where commentID ='"+ str(commentID) +"' ")
# articleID = cursor.fetchall()[0][0]
# cursor.execute("select * from demo_comments where articleID = '"+ str(articleID) +"' and commentID < '"+ str(commentID) +"' ")
#cursor.execute("select count(*) from comments")
cursor.execute("select demo_commentID from comments where commentID = '"+ str(commentID) +"'")
demo_commentID = cursor.fetchall()[0][0]
print demo_commentID
#cursor.execute("select * from comments limit 10")
for i in cursor:
    print i
# text_file = open("count.txt", "w")
# text_file.write(str(i[0]))
# text_file.close()
#
# count_read = open("count.txt", "r")
# print count_read.read()
# json_data = open("test.json")
#
# data = json.load(json_data)


cnx.close()
# #list1=[]
# #links = []
# comments = []
# csvFile = open("data/articles3.csv", 'Ur')
# csvReader = csv.reader(csvFile, delimiter=',', quotechar='"')
# #for row in range(500):
# #    list1.append(csvReader.next())
# for row in csvReader:
#     links.append(row[3])
#
# #for link in links:
# #    print link
#
# csvFile2 = open("data/comments_study.csv", 'Ur')
# csvReader2 = csv.reader(csvFile2, delimiter=',', quotechar='"')
# for data in csvReader2:
#     if data[10] in links:
#         comments.append(data)
#
# with open('data/comments_study3.csv', 'wb') as f:
#     writer = csv.writer(f)
#     for j in comments:
#         writer.writerows([j])
#
# #with open('data/articles3.csv', 'wb') as f:
# #    writer = csv.writer(f)
# #    for j in list1:
# #        writer.writerows([j])
