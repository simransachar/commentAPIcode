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
    # URL = "http://api.nytimes.com/svc/community/v2/comments/url/"
    URL = "http://api.nytimes.com/svc/community/v3/user-content/"

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
        params["replyLimit"] = "100"

        url = self.URL + "url" + ".json?" + urllib.urlencode (params)

        print url
        response = json.load(urllib.urlopen(url))
        self._LAST_CALL = time.time()
        self.nCalls += 1
        return response


def CollectComments():
    pagesize = 25
    rep_count = 0
    nytapi = NYTCommunityAPI(COMMUNITY_API_KEY2)
    offset = 0
    url2 = "http://www.nytimes.com/2015/03/05/upshot/what-is-the-next-next-silicon-valley.html"
    # Get the total # of comments for today
    r = nytapi.apiCall(url2, offset)
    totalCommentsFound = r["results"]["totalCommentsFound"]
    print "Total comments found: " + str(totalCommentsFound)
    fileWriter = csv.writer(open("article3Data.csv", "wb"),delimiter=",")
    header = ["userID","status","commentBody","approveDate","recommendationCount", \
                            "location","display_name","userComments","times_people", \
                            "commentSequence","editorsSelection","createDate"]
    fileWriter.writerow(header)
    # Loop through pages to get all comments
    while offset < totalCommentsFound:
        r = nytapi.apiCall(url2, offset)

        # DB insertion call here.
        if "comments" in r["results"]:
            for comment in r["results"]["comments"]:

                # userComments = escape_string(str(comment["userComments"].encode("utf8")))
                # userID = re.findall('([0-9]+).xml',userComments)
                userID = int(comment["userID"])
                commentBody = escape_string(str(comment["commentBody"].encode("utf8")))
                approveDate = int(comment["approveDate"])
                createDate = int(comment["createDate"])
                recommendationCount = int(comment["recommendations"])
                display_name = escape_string(str(comment["userDisplayName"].encode("utf8")))
                # userComments = escape_string(str(comment["userComments"].encode("utf8")))
                times_people = comment["timespeople"]

                # location = ""
                # if "location" in r:
                location = comment["userLocation"]
                if isinstance(location,int):
                    location = str(location)
                else:
                    location = escape_string(str(comment["userLocation"].encode("utf8")))
                commentSequence = int(comment["commentSequence"])
                status = escape_string(str(comment["status"].encode("utf8")))
                editorsSelection = int(comment["editorsSelection"])

                data = [userID,status,commentBody,approveDate,recommendationCount, \
                            location,display_name,"NA",times_people, \
                            commentSequence,editorsSelection,createDate]

                fileWriter.writerow(data)
                a = int(comment["replyCount"])
                print a
                print comment["replies"]
                if a > 3:
                    a = 3
                    print "replies: " + str(len(comment["replies"]))
                rep_count = rep_count + a
                if len(comment["replies"]) > 0:
                    for reply in comment["replies"]:

                        rep_userID = int(reply["userID"])
                        rep_commentBody = escape_string(str(reply["commentBody"].encode("utf8")))
                        rep_approveDate = int(reply["approveDate"])
                        rep_createDate = int(reply["createDate"])
                        rep_recommendationCount = int(reply["recommendations"])
                        rep_display_name = escape_string(str(reply["userDisplayName"].encode("utf8")))
                        # userComments = escape_string(str(comment["userComments"].encode("utf8")))
                        rep_times_people = reply["timespeople"]

                        # location = ""
                        # if "location" in r:
                        rep_location = reply["userLocation"]
                        if isinstance(rep_location,int):
                            rep_location = str(rep_location)
                        else:
                            rep_location = escape_string(str(reply["userLocation"].encode("utf8")))
                        rep_commentSequence = int(reply["commentSequence"])
                        rep_status = escape_string(str(reply["status"].encode("utf8")))
                        rep_editorsSelection = int(comment["editorsSelection"])
                        rep_data = [rep_userID,rep_status,rep_commentBody,rep_approveDate,rep_recommendationCount, \
                            rep_location,rep_display_name,"NA",rep_times_people, \
                            rep_commentSequence,rep_editorsSelection,rep_createDate]
                        fileWriter.writerow(rep_data)
        offset = offset + pagesize
        print "#Calls: " + str(nytapi.nCalls)
    print rep_count
CollectComments()