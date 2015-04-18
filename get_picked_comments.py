__author__ = 'simranjitsingh'

import csv

csvFile = open("article_data_picked_urls.csv", 'rb')
csvReader = csv.reader(csvFile, delimiter=',', quotechar='"')
count = 0
fileWriter = csv.writer(open("picked_comments2.csv", "wb"),delimiter=",")

for row in csvReader:

    if row[10] == '1':
        fileWriter.writerow(row)
        count = count + 1
        # if count > 999:
        #     break;
