__author__ = 'simranjitsingh'

import urllib
import json
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
params["id"] = "http://www.buzzfeed.com/floperry/things-you-only-know-if-youve-been-best-friends-for-10-ye"
params["id"] = "http://www.buzzfeed.com/ninamohan/this-violinist-mistakenly-thinking-she-won-an-award-will-giv#.cennXzQYRa"
params["access_token"] = "CAACEdEose0cBAAkOX3LsFF86rZCangYrl1qmeveE4FEoOwCIIRqHevCPGirxZCK6vvef2ZBT4rC8rpvPcpIk7HjpUSZBB89VKRjSx8sBIfFymK0WyU6GUmtuxVab3rRLsYOxP0ZAgVDkNaYSveQfZCnG67jzldCaSBLeUSfkCConWIkDb2vYiDw0Ffvllag3gZBHuJcbv909ZCdaPG9toSKkZBj4EL6JHh78ZD"
# params["fields"] = "og_object{comments}"

article_category ="politics"

req_url = URL + urllib.urlencode (params) + '&fields=og_object{comments}'
print req_url

response = json.load(urllib.urlopen(req_url))

for i in response["og_object"]["comments"]["data"]:

    commentID = i["id"]
    created_time = i["created_time"]
    like_count = i["like_count"]
    try:
        commentBody = escape_string(str(i["message"].encode("utf8")))
    except:
        commentBody = str(i["message"])

    userID = i["from"]["id"]
    display_name = i["from"]["name"]

    try:
        if isinstance(display_name,int):
            display_name = str(i["from"]["name"])
        elif display_name.isdigit():
            display_name = str(i["from"]["name"])
        else:
            display_name = escape_string(display_name.encode("utf8"))
    except:
        display_name = str(i["from"]["name"])

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
    print array

    insert_query = "INSERT INTO buzzfeed_comments (commentID, user_id, display_name," \
                   " user_first_name, gender,commentBody, like_count, created_time, article_category) " \
                   " VALUES('%s', %s, '%s','%s','%s', '%s','%d', '%s', '%s')" % \
                   (commentID, userID, display_name.decode("utf8"),userFirstName.decode("utf8"),
                     userGender, commentBody.decode("utf8"),like_count, created_time, article_category)

    cursor.execute(insert_query)

cnx.commit()