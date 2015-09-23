__author__ = 'simranjitsingh'

import json
import urllib
import mysql.connector
from ConfigParser import SafeConfigParser
import re
import sexmachine.detector as gender

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

genderObj = gender.Detector(case_sensitive=False)



def escape_string(string):
    res = string
    res = res.replace('\\','\\\\')
    res = res.replace('\n','\\n')
    res = res.replace('\r','\\r')
    res = res.replace('\047','\134\047') # single quotes
    res = res.replace('\042','\134\042') # double quotes
    res = res.replace('\032','\134\032') # for Win32
    return res

URL = "https://graph.facebook.com/v2.3/?"
params = {}
params["access_token"] = "CAACEdEose0cBAEZAmI7YZANTfCQkJ00Wv4ZAp9pT1osNmp6MQSdr0slodOdpSZCw5CcPOuqxFaBlhVAk7OykPHOs8cLb1EC7J0PzhqlOje6O87iiZABWGWV5wqZBZCB6mrN0h8SpPou17QYQEVS9GmBAfEUqOT4I35wPg1uhIyMsBLNChbBwCZBVeHW8TQqfbzyKqf4y9ZANGZCmcQKNwZBL0WHMfqsGOKbjF4ZD"

def collect_comments(response):
        try:
            data = response["og_object"]["comments"]["data"]
        except:
            print "the data is"
            data = response["data"]
            for k in data:
                print k

        for j in data:

            commentID = j["id"]
            cursor.execute("select count(*) from buzzfeed_comments where commentID = '"+ str(commentID) +"'")
            row_count = cursor.fetchall()[0][0]
            if row_count > 0:
                print "the record is already present, the row count is"
                print row_count
                continue

            created_time = j["created_time"]
            like_count = j["like_count"]
            try:
                commentBody = escape_string(str(j["message"].encode("utf8")))
            except:
                commentBody = str(j["message"])

            userID = j["from"]["id"]
            display_name = j["from"]["name"]

            try:
                if isinstance(display_name,int):
                    display_name = str(j["from"]["name"])
                elif display_name.isdigit():
                    display_name = str(j["from"]["name"])
                else:
                    display_name = escape_string(display_name.encode("utf8"))
            except:
                display_name = str(j["from"]["name"])

            name_split = re.findall(r'[aA-zZ]+',display_name)

            try:
                if len(name_split) == 0:
                    userFirstName = display_name
                else:
                    userFirstName = name_split[0]

                userFirstName = escape_string(str(userFirstName.encode("utf8")))
            except:
                userFirstName = display_name

            userGender = genderObj.get_gender(userFirstName)

            array = [commentID,created_time,like_count,commentBody,userID,display_name]
            # print array

            insert_query = "INSERT INTO buzzfeed_comments (commentID, user_id, display_name," \
                           " user_first_name, gender,commentBody, like_count, created_time, article_category,asset_URL) " \
                           " VALUES('%s', %s, '%s','%s','%s', '%s','%d', '%s', '%s', '%s')" % \
                           (commentID, userID, display_name.decode("utf8"),userFirstName.decode("utf8"),
                             userGender, commentBody.decode("utf8"),like_count, created_time, article_category,
                             assetURL.decode("utf8"))
            # try:
            cursor.execute(insert_query)
            # except:
            #     print "prob in insert"
            #     continue

        cnx.commit()
        try:
            comments_metadata = response["og_object"]["comments"]
        except:
            comments_metadata = response

        if "paging" in comments_metadata:
            print "--paging---"
            print comments_metadata["paging"]
            if "next" in comments_metadata["paging"]:
                print "--next---"
                next_url =  comments_metadata["paging"]["next"]
                response_next = json.load(urllib.urlopen(next_url))
                collect_comments(response_next)


with open("apidata/wtf.json") as json_file:

    json_data = json.load(json_file)
    article_category = json_data["channel"]["title"]
    print article_category
    for i in  json_data["channel"]["item"]:
        print i["link"]
        assetURL = escape_string(str(i["link"].encode('utf8')))
        params["id"] = i["link"]
        req_url = URL + urllib.urlencode (params) + '&fields=og_object{comments}'
        print req_url
        try:
            response = json.load(urllib.urlopen(req_url))
            for j in response["og_object"]["comments"]["data"]:
                print j
        except:
            continue

        collect_comments(response)


