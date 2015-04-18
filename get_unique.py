__author__ = 'simranjitsingh'

import csv


ID_list = []
# with open('article4_Data.csv', 'rb') as f:
#     reader = csv.reader(f)
#     ID_list = list(reader)

csvFile = open("picked_comments2.csv", 'rb')
csvReader = csv.reader(csvFile, delimiter=',', quotechar='"')

for row in csvReader:
    if csvReader.line_num > 1:
        ID_list.append(row[0])

print len(ID_list)

#ID_list = list(zip(*ID_list)[0])

myset = set(ID_list)

mynewlist = list(myset)

print len(mynewlist)

fileWriter = csv.writer(open("unique_userIDs_picked_comments.csv", "wb"),delimiter=",")

for ID in mynewlist:
   fileWriter.writerow([ID])

