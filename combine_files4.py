__author__ = 'simranjitsingh'

import csv


csvFile1 = open("picked_comments2.csv", 'rb')
csvReader1 = csv.reader(csvFile1, delimiter=',', quotechar='"')

csvFile2 = open("picked_userscores_deok.csv", 'rb')
csvReader2 = csv.reader(csvFile2, delimiter=',', quotechar='"')

fileWriter = csv.writer(open("picked_comments_user_scores.csv", "wb"),delimiter=",")
list1 =[]
list2=[]


for row in csvReader1:
    if csvReader1.line_num > 1:
        list1.append(row)

for row in csvReader2:
    # if csvReader2.line_num > 1:
        list2.append(row)

for data in list1:
    # final_list = data + [0,0,0,0,0,0]
    for v in list2:
        if v[0] == data[0]:
           v.pop(0)
           final_list = data + v
    fileWriter.writerow(final_list)
