__author__ = 'simranjitsingh'

import csv
import urllib
import json
from ConfigParser import SafeConfigParser
import time
import mysql.connector

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
parserkeys.read('apidata/keys_config_newswire.ini')

# Fetch the key values from config file (depends upon how many api keys you have)
key_list =  parserkeys.options('API-KEYS')
COMMUNITY_API_KEY_LIST = [parserkeys.get('API-KEYS', key) for key in key_list]
# COMMUNITY_API_KEY_LIST = COMMUNITY_API_KEY_LIST[::-1]

key_limit = 4990

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
    URL = "http://api.nytimes.com/svc/news/v3/content"
    def __init__(self,key):
        self.nQueries = 0
        self.api_key = key
        self.QUERY_LIMIT = 30
        self.LAST_CALL = 0
        self.nCalls = 0;

    def apiCall(self, article_url):
        interval = self.LAST_CALL - time.time()
        if interval < 1:
            self.nQueries += 1
            if self.nQueries >= self.QUERY_LIMIT:
                time.sleep (1)
                self.nQueries = 0

        params = {}
        params["url"] = article_url
        params["api-key"] = self.api_key

        url = self.URL +  ".json?" + urllib.urlencode (params)
        print url
        response = json.load(urllib.urlopen(url))
        self._LAST_CALL = time.time()
        self.nCalls += 1
        return response

def CollectComments():

        key_index = 0
        API_KEY = COMMUNITY_API_KEY_LIST[key_index]
        nytapi = NYTCommunityAPI(API_KEY)

        csvFile1 = open("apidata/articleURLs.csv", 'rb')
        csvReader1 = csv.reader(csvFile1, delimiter=',', quotechar='"')

        count = 1
        s = ""
        for row in csvReader1:
            print row[0]
            cursor.execute("select count(*) from nyt_articles_all where articleURL = '"+ str(row[0]) +"'")
            row_count = cursor.fetchall()[0][0]
            if row_count > 0:
                print "the url is already present, the row count is"
                print row_count
                continue

            r = nytapi.apiCall(row[0])
            if len(r["results"]) < 1:
                print "#Calls: " + str(nytapi.nCalls)
                print "counter value: " + str(count)
                count += 1
                continue

            print r["results"][0]
            section = r["results"][0]["section"]
            subsection = r["results"][0]["subsection"]
            title = escape_string(r["results"][0]["title"])
            abstract = escape_string(r["results"][0]["abstract"].encode('utf8'))
            item_type = r["results"][0]["item_type"]
            updateDate = r["results"][0]["updated_date"]
            createDate = r["results"][0]["created_date"]
            publishedDate = r["results"][0]["published_date"]
            materialTypeFacet = r["results"][0]["material_type_facet"]
            kicker = r["results"][0]["kicker"]
            des_facet = r["results"][0]["des_facet"]
            if len(des_facet) > 0:
                des_facet = escape_string(str(r["results"][0]["des_facet"]))

            org_facet = r["results"][0]["org_facet"]
            if len(org_facet) > 0:

                org_facet = escape_string(str(r["results"][0]["org_facet"]))

            per_facet = r["results"][0]["per_facet"]
            if len(per_facet) > 0:
                per_facet = escape_string(str(r["results"][0]["per_facet"]))

            geo_facet = r["results"][0]["geo_facet"]
            if len(geo_facet) > 0:
                geo_facet = escape_string(str(r["results"][0]["geo_facet"]))

            insert_query = "INSERT INTO nyt_articles_all ( articleURL, section, subsection, " \
               "title, abstract, item_type, updateDate, createDate, publishedDate, " \
               "materialTypeFacet, kicker, des_facet, org_facet, per_facet, geo_facet)" \
               " VALUES( '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', " \
               "'%s', '%s', '%s', '%s', '%s', '%s', '%s')" % \
               (row[0], section, subsection,title,
                abstract.decode("utf8"), item_type,updateDate, createDate, publishedDate,
                materialTypeFacet, kicker, des_facet,
                org_facet, per_facet, geo_facet)


            cursor.execute(insert_query)
            cnx.commit()
            if count >= key_limit:
                    key_index += 1
                    count = 0
                    if key_index >= len(COMMUNITY_API_KEY_LIST):
                        print "loop break"
                        break;
                    API_KEY = COMMUNITY_API_KEY_LIST[key_index]
                    nytapi = NYTCommunityAPI(API_KEY)

#                    r = nytapi.apiCall(row[0])
            print "#Calls: " + str(nytapi.nCalls)
            print "counter value: " + str(count)
            count += 1

CollectComments()