__author__ = 'simranjitsingh'

import csv
import operator
new_list=[]
mini_list=[]
reader = csv.reader(open("data/vocab3.csv"), delimiter=",")
i = 0
for j in reader:
    a = int(j[1])
    mini_list.append(j[0])
    mini_list.append(a)
    new_list.append(mini_list)
    mini_list = []

sortedlist = sorted(new_list, key=operator.itemgetter(1), reverse=True)
#sortedlist = reader

with open('data/vocab4.csv', 'wb') as f:
    writer = csv.writer(f)
    for j in sortedlist:
        writer.writerows([j])