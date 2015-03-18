__author__ = 'simranjitsingh'

import csv

ID_list = []

csvFile = open("article5_Data.csv", 'rb')
csvReader = csv.reader(csvFile, delimiter=',', quotechar='"')

fileWriter = csv.writer(open("article5_picked_users.csv", "wb"),delimiter=",")



for row in csvReader:
    if csvReader.line_num > 1:
        if row[10] == '1':
            ID_list.append(row[0])

print len(ID_list)

#ID_list = list(zip(*ID_list)[0])

myset = set(ID_list)

mynewlist = list(myset)

print len(mynewlist)

fileWriter = csv.writer(open("article5_picked_users.csv", "wb"),delimiter=",")

for ID in mynewlist:
   fileWriter.writerow([ID])



