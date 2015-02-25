__author__ = 'simranjitsingh'

import urllib
import urllib2
import json
import random
from time import sleep
import csv

url = 'http://205.188.201.176/geocoding/v1/address?key=Fmjtd%7Cluur2968ng%2Cr0%3Do5-90rs54&'

csvFile = open("articleData_geocode.csv", 'Ur')
csvReader = csv.reader(csvFile, delimiter=',', quotechar='"')
fileWriter = csv.writer(open("articleData_geocode2.csv", "ab"),delimiter=",")

for row in csvReader:
    if csvReader.line_num > 1:
        if row[17] == "NA":
            loc = row[5]
            purl = url + urllib.urlencode({"location": loc})
            print purl
            #r = requests.get(purl)
            #rjson = json.loads(r.text)
            request = urllib2.Request(purl)
            res = urllib2.urlopen(request)
            rjson = json.loads(res.read())
            res.close()
            if len(rjson["results"][0]["locations"]) > 0:
                top_location = rjson["results"][0]["locations"][0]
                lat = top_location["latLng"]["lat"]
                lng = top_location["latLng"]["lng"]
                lat_lon = [lat,lng]
                row[17] = lat
                row[18] = lng
                print lat_lon
                fileWriter.writerow(row)
            sleep(random.randrange(100,101) / 1000)