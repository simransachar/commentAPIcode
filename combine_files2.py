__author__ = 'simranjitsingh'

import csv


csvFile1 = open("article5_Data_withScores_geocode.csv", 'rb')
csvReader1 = csv.reader(csvFile1, delimiter=',', quotechar='"')

csvFile2 = open("picked_userscores_article5.csv", 'rb')
csvReader2 = csv.reader(csvFile2, delimiter=',', quotechar='"')

header = ["UserID","Status_Accepted","commentBody","ApproveDate","RecommendationCount", \
                            "Location","DisplayName","UserComments","TimesPeople", \
                            "CommentSequence","EditorsSelection","ArticleRelevance","ConversationalRelevance", \
                            "PersonalXP","Readability","Brevity","RecommendationScore","Latitude", "Longitude", "AVGPersonalXP", \
                            "AVGReadability","AVGBrevity","AVGRecommendationScore","AVGPicks","AVGcommentspermonth"]


fileWriter = csv.writer(open("article5_final.csv", "wb"),delimiter=",")
fileWriter.writerow(header)
list1 =[]
list2=[]


for row in csvReader1:
    if csvReader1.line_num > 1:
        list1.append(row)

for row in csvReader2:
    if csvReader2.line_num > 1:
        list2.append(row)


for data in list1:
    final_list = data + [0,0,0,0,0,0]
    for v in list2:
        if v[0] == data[0]:
           v.pop(0)
           final_list = data + v
    fileWriter.writerow(final_list)

