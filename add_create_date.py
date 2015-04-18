__author__ = 'simranjitsingh'

import csv

csvFile1 = open("article1Data.csv", 'rb')
csvReader1 = csv.reader(csvFile1, delimiter=',', quotechar='"')

csvFile2 = open("article1_final_normalized.csv", 'rb')
csvReader2 = csv.reader(csvFile2, delimiter=',', quotechar='"')

list1 =[]
list2=[]

fileWriter = csv.writer(open("article1_createDate.csv", "wb"),delimiter=",")

header = ["createDate","UserID","Status_Accepted","commentBody","ApproveDate","RecommendationCount", \
                            "Location","DisplayName","UserComments","TimesPeople", \
                            "CommentSequence","EditorsSelection","ArticleRelevance","ConversationalRelevance", \
                            "PersonalXP","Readability","Brevity","RecommendationScore","Latitude", "Longitude", "userID","AVGPersonalXP", \
                            "AVGReadability","AVGBrevity","AVGRecommendationScore","AVGPicks","AVGcommentspermonth"]
fileWriter.writerow(header)
for row in csvReader1:
    if csvReader1.line_num > 1:
        list1.append(row)

for row in csvReader2:
    if csvReader2.line_num > 1:
        list2.append(row)

for row in list2:
    data = ["NA"] + row
    for row2 in list1:
        if row[9] == row2[9]:
            data = [row2[9]] + row


    fileWriter.writerow(data)
