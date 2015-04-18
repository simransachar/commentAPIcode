__author__ = 'simranjitsingh'

import csv

csvFile1 = open("comments_study.csv", 'rb')
csvReader1 = csv.reader(csvFile1, delimiter=',', quotechar='"')

csvFile2 = open("AR_CR.csv", 'rb')
csvReader2 = csv.reader(csvFile2, delimiter=',', quotechar='"')

fileWriter = csv.writer(open("AR_CR_withBody.csv", "wb"),delimiter=",")

dict1={}

for row in csvReader1:
    dict1[row[8]] = row[2]

for row in csvReader2:
    row[2] = dict1[row[8]]
    fileWriter.writerow(row)
