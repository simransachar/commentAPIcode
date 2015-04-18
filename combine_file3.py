__author__ = 'simranjitsingh'

import csv


csvFile1 = open("comment_study_article_relevance.csv", 'rb')
csvReader1 = csv.reader(csvFile1, delimiter=',', quotechar='"')

csvFile2 = open("comment_study_comment_conversational_relevance.csv", 'rb')
csvReader2 = csv.reader(csvFile2, delimiter=',', quotechar='"')

header = ["UserID","Status_Accepted","commentBody","ApproveDate","RecommendationCount", \
                            "Location","DisplayName","UserComments","TimesPeople", \
                            "CommentSequence","EditorsSelection","ArticleRelevance","ConversationalRelevance", \
                            "PersonalXP","Readability","Brevity","RecommendationScore","Latitude", "Longitude", "userID","AVGPersonalXP", \
                            "AVGReadability","AVGBrevity","AVGRecommendationScore","AVGPicks","AVGcommentspermonth"]


fileWriter = csv.writer(open("AR_CR.csv", "wb"),delimiter=",")
fileWriter.writerow(header)
list1 =[]
list2=[]
dict_ar ={}
dict_cr ={}

for row in csvReader1:
    # if csvReader1.line_num > 1:
    #     list1.append(row)
    dict_ar[row[8]] = row[13]

for row in csvReader2:
    # if csvReader2.line_num > 1:
    #     list2.append(row)
    dict_cr[row[8]] = row[13]

    ar_value = dict_ar[row[8]]
    row.append(ar_value)
    fileWriter.writerow(row)
    # print final_list

# for row in csvReader2:
#     print row
#     ar_value = dict_ar[row[8]]
#     final_list = row.extend(ar_value)
#     fileWriter.writerow(final_list)
#     print final_list
# for data in list1:
# #    print data
#     for v in list2:
#
#         if v[4] == data[8]:
#
#            final_list = data + list(v[8])
#            print "-------------"
#            print final_list
#            print "-------------"
#            fileWriter.writerow(final_list)