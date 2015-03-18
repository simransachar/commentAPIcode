# -*- coding: utf-8 -*-

# This code scrap the data from NYT API via the API keys and  stored in vocab_comments table
# Frequency of each word is calculated from stored data and output in a JSON
# Count the number of comments and store in a text file

__author__ = 'simranjitsingh'
import urllib
import time
import datetime
import json
import mysql.connector
import sys
import re
from nltk.corpus import stopwords
import nltk.tag, nltk.util, nltk.stem
from ConfigParser import SafeConfigParser
import csv

# Get the config file for database
parserDb = SafeConfigParser()
# Edit the config file to fill in your credentials
parserDb.read('apidata/database.ini')

# Fetch the credentials from config file
user = parserDb.get('credentials', 'user')
password = parserDb.get('credentials', 'password')
host = parserDb.get('credentials', 'host')
database = parserDb.get('credentials', 'database')

cnx = mysql.connector.connect(user=user, password=password, host=host, database=database)
cursor = cnx.cursor()

# Get the config file for NYT Api Key/keys
parserkeys = SafeConfigParser()
# Edit the config file to fill in your api keys and values
parserkeys.read('apidata/keys_config.ini')

# Fetch the key values from config file (depends upon how many api keys you have)
COMMUNITY_API_KEY = parserkeys.get('API-KEYS', 'KEY1')
COMMUNITY_API_KEY2 = parserkeys.get('API-KEYS', 'KEY2')
COMMUNITY_API_KEY3 = parserkeys.get('API-KEYS', 'KEY3')
COMMUNITY_API_KEY4 = parserkeys.get('API-KEYS', 'KEY4')


COMMUNITY_API_KEY_LIST = [COMMUNITY_API_KEY,COMMUNITY_API_KEY2,COMMUNITY_API_KEY3,COMMUNITY_API_KEY4]
key_limit = 4500

doc_frequency = {}
stopword_list = stopwords.words('english')
porter = nltk.PorterStemmer()

global g_offset
global g_ID
g_offset = None
g_ID = None

def error_name(g_offset,ID):
    exc_type, exc_obj, exc_tb = sys.exc_info()
    msg = str(exc_type)
    error = re.split(r'[.]',msg)
    error = re.findall(r'\w+',error[1])
    error_msg = str(error[0]) + "occured in line " + str(exc_tb.tb_lineno) + " " \
                ",offset: " + str(g_offset) + " , userID: " + str(ID)
    return error_msg

def escape_string(string):
    res = string
    res = res.replace('\\','\\\\')
    res = res.replace('\n','\\n')
    res = res.replace('\r','\\r')
    res = res.replace('\047','\134\047') # single quotes
    res = res.replace('\042','\134\042') # double quotes
    res = res.replace('\032','\134\032') # for Win32
    return res

class NYTCommunityAPI (object):
    URL = "http://api.nytimes.com/svc/community/v2/comments/user/id/"
    def __init__(self,key):
        self.nQueries = 0
        self.api_key = key
        self.QUERY_LIMIT = 30
        self.LAST_CALL = 0
        self.nCalls = 0;

    def apiCall(self, ID, offset=0):
        interval = self.LAST_CALL - time.time()
        if interval < 1:
            self.nQueries += 1
            if self.nQueries >= self.QUERY_LIMIT:
                time.sleep (1)
                self.nQueries = 0

        params = {}
        params["api-key"] = self.api_key
        params["offset"] = str(offset)
        params["sort"] = "oldest"

        url = self.URL + ID + ".json?" + urllib.urlencode (params)
        print url
        response = json.load(urllib.urlopen(url))
        self._LAST_CALL = time.time()
        self.nCalls += 1
        return response

# This code scrap the data from NYT API via the API keys and  stored in vocab_comments table
def CollectComments():
    # try:
        pagesize = 25
        key_index = 0
        API_KEY = COMMUNITY_API_KEY_LIST[key_index]
        nytapi = NYTCommunityAPI(API_KEY)
        global g_offset
        global g_ID
        count = 0
        with open('new_article5_picked_users_work.csv', 'rb') as f:
            reader = csv.reader(f)
            ID_list = list(reader)
        fileWriter = csv.writer(open("picked_user_comments_article5.csv", "ab"),delimiter=",")
        header = ["userID","status","commentBody","approveDate","recommendationCount", \
                            "location","display_name","userComments","times_people", \
                            "commentSequence","editorsSelection"]
        # fileWriter.writerow(header)
        g_offset = 0
        g_ID = ID_list[0][0]

        for ID in ID_list:
            ID = ID[0]
            offset = 0

            #Get the total # of comments for today
            r = nytapi.apiCall(ID, offset)
            totalCommentsFound = r["results"]["totalCommentsFound"]
            print "Total comments found: " + str(totalCommentsFound)
            count += 1
            # Loop through pages to get all comments
            while offset < totalCommentsFound:
                g_offset = offset
                g_ID = ID
                if count >= key_limit:
                    key_index += 1
                    count = 0
                    if key_index >= len(COMMUNITY_API_KEY_LIST):
                        print "last offset value: " + str(offset-25)
                        print "usedID: " + str(ID)
                        print "total comments by user: " + str(totalCommentsFound)
                        sys.exit(0)
                    API_KEY = COMMUNITY_API_KEY_LIST[key_index]
                    nytapi = NYTCommunityAPI(API_KEY)

                r = nytapi.apiCall(ID, offset)
                # DB insertion call here.
                if "comments" in r["results"]:
                    for comment in r["results"]["comments"]:
                        commentBody = escape_string(str(comment["commentBody"].encode("utf8")))
                        # approveDate = int(comment["approveDate"])
                        approveDate = comment["approveDate"]
                        recommendationCount = int(comment["recommendations"])
                        times_people = int(comment["times_people"])
                        display_name = escape_string(str(comment["display_name"].encode("utf8")))
                        # location = ""
                        # if "location" in r:
                        location = escape_string(str(comment["location"].encode("utf8")))
                        commentSequence = comment["commentSequence"]
                        if isinstance(commentSequence, int):
                            commentSequence = int(commentSequence)
                        else:
                            commentSequence = 0

                        if approveDate is None:
                            approveDate = 0
                        else:
                            approveDate = int(approveDate)

                        status = escape_string(str(comment["status"].encode("utf8")))
                        editorsSelection = int(comment["editorsSelection"])
                        userComments = escape_string(str(comment["userComments"].encode("utf8")))
                        userID = re.findall('([0-9]+).xml',userComments)
                        userID = int(userID[0])
                        insert_query = "INSERT INTO user_comments (status, commentSequence, commentBody," \
                                       " approveDate, recommendationCount, editorsSelection, display_name," \
                                       " location, user_comment,time_people,user_id)" \
                                       " VALUES('%s', %d, '%s', FROM_UNIXTIME(%d), %d, %d, '%s', '%s', '%s','%d','%d')" % \
                                       (status.decode("utf8"), commentSequence, commentBody.decode("utf8"), approveDate,
                                        recommendationCount, editorsSelection, display_name.decode("utf8"),
                                        location.decode("utf8"), userComments.decode("utf8"),times_people,userID)

                        cursor.execute(insert_query)
                        csv_data = [userID,status,commentBody,approveDate,recommendationCount, \
                            location,display_name,userComments,times_people, \
                            commentSequence,editorsSelection]

                        fileWriter.writerow(csv_data)

                cnx.commit()
                offset = offset + pagesize
                count += 1
                print "#Calls: " + str(nytapi.nCalls)
                print "counter value: " + str(count)
            # Go to next day
    # except:
    #     print error_name(g_offset,g_ID)
    #     sys.exit(1)


CollectComments()


