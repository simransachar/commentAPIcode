__author__ = 'simranjitsingh'

import csv


csvFile1 = open("AR_CR_others_normalized.csv", 'rb')
csvReader1 = csv.reader(csvFile1, delimiter=',', quotechar='"')

csvFile2 = open("picked_comments_user_scores_normalized.csv", 'rb')
csvReader2 = csv.reader(csvFile2, delimiter=',', quotechar='"')

header = ["CommentID","CommentTitle","commentBody","ApproveDate","RecommendationCount", \
                            "DisplayName","Location", "CommentsQuestion","CommentSequence","status", \
                            "articleURL","EditorsSelection","in_study","ArticleRelevance","ConversationalRelevance", \
                            "PersonalXP","Readability","Brevity","RecommendationScore", "AVGPersonalXP", \
                            "AVGReadability","AVGBrevity","AVGRecommendationScore","AVGPicks","AVGcommentspermonth"]


fileWriter = csv.writer(open("1034_picked_comments_final_normalized.csv", "wb"),delimiter=",")
fileWriter.writerow(header)
list1 =[]
list2=[]


for row in csvReader1:
    # if csvReader1.line_num > 1:
        list1.append(row)

for row in csvReader2:
    # if csvReader2.line_num > 1:
        list2.append(row)


for data in list1:
    final_list = data + ["NA","NA","NA","NA","NA","NA"]
    for v in list2:
        if v[9] == data[8]:
           user_scores = [v[11],v[12],v[13],v[14],v[15],v[16]]
           final_list = data + user_scores
    fileWriter.writerow(final_list)

