__author__ = 'simranjitsingh'

import csv

csvFile1 = open("AR_CR_others.csv", 'rb')
csvReader1 = csv.reader(csvFile1, delimiter=',', quotechar='"')

list1 = []

header = ["UserID","Status_Accepted","commentBody","ApproveDate","RecommendationCount", \
                            "Location","DisplayName","UserComments","TimesPeople", \
                            "CommentSequence","EditorsSelection","ArticleRelevance","ConversationalRelevance", \
                            "PersonalXP","Readability","Brevity","RecommendationScore","Latitude", "Longitude","AVGPersonalXP", \
                            "AVGReadability","AVGBrevity","AVGRecommendationScore","AVGPicks","AVGcommentspermonth"]


fileWriter = csv.writer(open("AR_CR_others_normalized.csv", "wb"),delimiter=",")
# fileWriter.writerow(header)


for i in csvReader1:
    # if csvReader1.line_num > 1:
        list1.append(i)


ar_list = []
cr_list=[]

px_list=[]

read_list=[]

br_list=[]

rec_list=[]

avg_px_list=[]

avg_read_list=[]

avg_br_list=[]

avg_rec_list=[]

avg_picks_list=[]

avg_month_list=[]

for i in list1:

    ar_list.append(float(i[17]))

    cr_list.append(float(i[18]))

    px_list.append(float(i[13]))

    read_list.append(float(i[14]))

    br_list.append(float(i[15]))

    rec_list.append(float(i[16]))

    # avg_px_list.append(float(i[17]))
    #
    # avg_read_list.append(float(i[18]))
    #
    # avg_br_list.append(float(i[21]))
    #
    # avg_rec_list.append(float(i[22]))
    #
    # avg_picks_list.append(float(i[23]))
    #
    # avg_month_list.append(float(i[24]))

counter = 0
for i in list1:

    d = max(ar_list) - min(ar_list)
    d2 = float(i[17]) - float(min(ar_list))
    net_score = (100/float(d)) * d2
    loc1 = list1.index(i)
    list1[loc1][17] = net_score

    d = max(cr_list) - min(cr_list)
    d2 = float(i[18]) - float(min(cr_list))
    net_score = (100/float(d)) * d2
    loc1 = list1.index(i)
    list1[loc1][18] = net_score

    d = max(px_list) - min(px_list)
    d2 = float(i[13]) - float(min(px_list))
    net_score = (100/float(d)) * d2
    loc1 = list1.index(i)
    list1[loc1][13] = net_score

    d = max(read_list) - min(read_list)
    d2 = float(i[14]) - float(min(read_list))
    net_score = (100/float(d)) * d2
    loc1 = list1.index(i)
    list1[loc1][14] = net_score

    d = max(br_list) - min(br_list)
    d2 = float(i[15]) - float(min(br_list))
    net_score = (100/float(d)) * d2
    loc1 = list1.index(i)
    list1[loc1][15] = net_score

    d = max(rec_list) - min(rec_list)
    d2 = float(i[16]) - float(min(rec_list))
    net_score = (100/float(d)) * d2
    loc1 = list1.index(i)
    list1[loc1][16] = net_score

    # d = max(avg_px_list) - min(avg_px_list)
    # d2 = float(i[19]) - float(min(avg_px_list))
    # net_score = (100/float(d)) * d2
    # loc1 = list1.index(i)
    # list1[loc1][19] = net_score
    #
    # d = max(avg_read_list) - min(avg_read_list)
    # d2 = float(i[20]) - float(min(avg_read_list))
    # net_score = (100/float(d)) * d2
    # loc1 = list1.index(i)
    # list1[loc1][20] = net_score
    #
    # d = max(avg_br_list) - min(avg_br_list)
    # d2 = float(i[21]) - float(min(avg_br_list))
    # net_score = (100/float(d)) * d2
    # loc1 = list1.index(i)
    # list1[loc1][21] = net_score
    #
    # d = max(avg_rec_list) - min(avg_rec_list)
    # d2 = float(i[22]) - float(min(avg_rec_list))
    # net_score = (100/float(d)) * d2
    # loc1 = list1.index(i)
    # list1[loc1][22] = net_score
    #
    # d = max(avg_picks_list) - min(avg_picks_list)
    # d2 = float(i[23]) - float(min(avg_picks_list))
    # net_score = (100/float(d)) * d2
    # loc1 = list1.index(i)
    # list1[loc1][23] = net_score
    #
    # d = max(avg_month_list) - min(avg_month_list)
    # d2 = float(i[24]) - float(min(avg_month_list))
    # net_score = (100/float(d)) * d2
    # loc1 = list1.index(i)
    # list1[loc1][24] = net_score
    print i
    fileWriter.writerow(i)