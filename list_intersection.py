__author__ = 'simranjitsingh'

import csv


with open('total_unique_userIDs.csv', 'rb') as f:
    reader = csv.reader(f)
    ID_list = list(reader)

ID_list = list(zip(*ID_list)[0])

total_myset = set(ID_list)


with open('article5_picked_users.csv', 'rb') as f:
    reader = csv.reader(f)
    ID_list2 = list(reader)

ID_list2 = list(zip(*ID_list2)[0])

current_set = set(ID_list2)



exclude_list = list(set(total_myset).intersection(current_set))

print exclude_list
print len(current_set)

total_unique_id_list = list(total_myset)

net_user_ids = current_set - set(exclude_list)
print len(net_user_ids)
net_user_ids = list(net_user_ids)
print len(total_unique_id_list)
total_unique_id_list = total_unique_id_list + net_user_ids
print len(total_unique_id_list)


fileWriter = csv.writer(open("new_article5_picked_users.csv", "wb"),delimiter=",")

for ID in net_user_ids:
   fileWriter.writerow([ID])

fileWriter = csv.writer(open("total_unique_userIDs.csv", "wb"),delimiter=",")

for ID1 in total_unique_id_list:
   fileWriter.writerow([ID1])
