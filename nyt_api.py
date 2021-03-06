# -*- coding: utf-8 -*-
__author__ = 'simranjitsingh'

import urllib
import time
import datetime
import json
import mysql.connector

cnx = mysql.connector.connect(user='root', password='simran',
                              host='127.0.0.1',
                              database='comment_iq')
cursor = cnx.cursor()
COMMUNITY_API_KEY2 = "6adcef7a975045db61389446ca15283e:1:30173638"

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
    URL = "http://api.nytimes.com/svc/community/v2/comments/by-date/"

    def __init__(self, key):
        self.nQueries = 0
        self.api_key = key
        self.QUERY_LIMIT = 30
        self.LAST_CALL = 0
        self.nCalls = 0;

    def apiCall(self, date, offset=0):
        interval = self.LAST_CALL - time.time()
        if interval < 1:
            self.nQueries += 1
            if self.nQueries >= self.QUERY_LIMIT:
                time.sleep (1)
                self.nQueries = 0

        # set parameters
        params = {}
        params["api-key"] = self.api_key
        params["offset"] = str(offset)
        params["sort"] = "oldest"

        url = self.URL + date + ".json?" + urllib.urlencode (params)

        print url
        response = json.load(urllib.urlopen(url))
        self._LAST_CALL = time.time()
        self.nCalls += 1
        return response


def CollectComments():
    pagesize = 25
    nytapi = NYTCommunityAPI(COMMUNITY_API_KEY2)
    # originally started collection from 20140115
    d_start = datetime.date(2015,02,01)
    d_end = datetime.date(2015,02,02)
    d = d_start
    while d < d_end:
        offset = 0
        date_string = d.strftime("%Y%m%d")

        # Get the total # of comments for today
        r = nytapi.apiCall(date_string, offset)
        totalCommentsFound = r["results"]["totalCommentsFound"]
        print "Total comments found: " + str(totalCommentsFound)

        # Loop through pages to get all comments
        while offset < totalCommentsFound:
            r = nytapi.apiCall(date_string, offset)

            # DB insertion call here.
            if "comments" in r["results"]:
                for comment in r["results"]["comments"]:

                    commentBody = escape_string(str(comment["commentBody"].encode("utf8")))
                    approveDate = int(comment["approveDate"])
                    recommendationCount = int(comment["recommendationCount"])
                    display_name = escape_string(str(comment["display_name"].encode("utf8")))
                    userComments = escape_string(str(comment["userComments"].encode("utf8")))

                    location = ""
                    if "location" in r:
                        location = escape_string(str(comment["location"].encode("utf8")))
                    commentSequence = int(comment["commentSequence"])
                    status = escape_string(str(comment["status"].encode("utf8")))
                    articleURL = escape_string(str(comment["articleURL"].encode('utf8')))
                    editorsSelection = int(comment["editorsSelection"])
                    params = {}
                    params["url"] = "http://www.nytimes.com/2015/02/13/us/politics/fbi-director-comey-speaks-frankly-about-police-view-of-blacks.html"
                    url = ".json?" + urllib.urlencode (params)
                    print url
                    insert_query = "INSERT INTO comments (status, commentSequence, commentBody, approveDate, recommendationCount, editorsSelection, display_name, location, articleURL) VALUES('%s', %d, '%s', FROM_UNIXTIME(%d), %d, %d, '%s', '%s', '%s')" % (status.decode("utf8"), commentSequence, commentBody.decode("utf8"), approveDate, recommendationCount, editorsSelection, display_name.decode("utf8"), location.decode("utf8"), articleURL.decode("utf8"))
                    cursor.execute(insert_query)
    #				dbc.execute(insert_query)

            offset = offset + pagesize
            print "#Calls: " + str(nytapi.nCalls)

        # Go to next day
        d += datetime.timedelta(days=1)

CollectComments()