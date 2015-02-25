# -*- coding: utf-8 -*-
__author__ = 'simranjitsingh'

import urllib
import time
import datetime
import json
import mysql.connector
import re
import csv

cnx = mysql.connector.connect(user='merrillawsdb', password='WR3QZGVaoHqNXAF',
                              host='awsdbinstance.cz5m3w6kwml8.us-east-1.rds.amazonaws.com',
                              database='comment_iq')

# cnx = mysql.connector.connect(user='root', password='simran',
#                               host='127.0.0.1',
#                               database='comment_iq')

cursor = cnx.cursor()
COMMUNITY_API_KEY2 = "5a3d3ff964c9975c0f23d1ad3437dd45:0:70179423"


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
    URL = "http://api.nytimes.com/svc/community/v2/comments/url/"

    def __init__(self, key):
        self.nQueries = 0
        self.api_key = key
        self.QUERY_LIMIT = 30
        self.LAST_CALL = 0
        self.nCalls = 0;

    def apiCall(self, url2, offset=0):
        interval = self.LAST_CALL - time.time()
        if interval < 1:
            self.nQueries += 1
            if self.nQueries >= self.QUERY_LIMIT:
                time.sleep (1)
                self.nQueries = 0

        # set parameters
        params = {}
        params["url"] = url2
        params["api-key"] = self.api_key
        params["offset"] = str(offset)
        params["sort"] = "oldest"


        url = self.URL + "exact-match" + ".json?" + urllib.urlencode (params)

        print url
        response = json.load(urllib.urlopen(url))
        self._LAST_CALL = time.time()
        self.nCalls += 1
        return response


def CollectComments():
    pagesize = 25
    nytapi = NYTCommunityAPI(COMMUNITY_API_KEY2)
    offset = 0
    url2 = "http://www.nytimes.com/2015/02/13/us/politics/fbi-director-comey-speaks-frankly-about-police-view-of-blacks.html"
    # Get the total # of comments for today
    r = nytapi.apiCall(url2, offset)
    totalCommentsFound = r["results"]["totalCommentsFound"]
    print "Total comments found: " + str(totalCommentsFound)
    fileWriter = csv.writer(open("articleData2.csv", "wb"),delimiter=",")
    header = ["userID","status","commentBody","approveDate","recommendationCount", \
                            "location","display_name","userComments","times_people", \
                            "commentSequence","editorsSelection"]
    fileWriter.writerow(header)
    # Loop through pages to get all comments
    while offset < totalCommentsFound:
        r = nytapi.apiCall(url2, offset)

        # DB insertion call here.
        if "comments" in r["results"]:
            for comment in r["results"]["comments"]:

                userComments = escape_string(str(comment["userComments"].encode("utf8")))
                userID = re.findall('([0-9]+).xml',userComments)
                userID = userID[0]
                commentBody = escape_string(str(comment["commentBody"].encode("utf8")))
                approveDate = int(comment["approveDate"])
                recommendationCount = int(comment["recommendations"])
                display_name = escape_string(str(comment["display_name"].encode("utf8")))
                userComments = escape_string(str(comment["userComments"].encode("utf8")))
                times_people = comment["times_people"]

                # location = ""
                # if "location" in r:
                location = escape_string(str(comment["location"].encode("utf8")))
                commentSequence = int(comment["commentSequence"])
                status = escape_string(str(comment["status"].encode("utf8")))
                editorsSelection = int(comment["editorsSelection"])

                data = [userID,status,commentBody,approveDate,recommendationCount, \
                            location,display_name,userComments,times_people, \
                            commentSequence,editorsSelection]

                fileWriter.writerow(data)
        offset = offset + pagesize
        print "#Calls: " + str(nytapi.nCalls)

CollectComments()