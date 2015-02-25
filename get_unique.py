__author__ = 'simranjitsingh'

import csv

with open('userIDs.csv', 'rb') as f:
    reader = csv.reader(f)
    ID_list = list(reader)

ID_list = list(zip(*ID_list)[0])

myset = set(ID_list)

mynewlist = list(myset)


fileWriter = csv.writer(open("unique_userIDs.csv", "wb"),delimiter=",")

for ID in mynewlist:
   fileWriter.writerow([ID])

