__author__ = 'simranjitsingh'

import ijson
import json

f = open('yelp2.json')
objects = ijson.items(f, 'earth.europe.item')
cities = (o for o in objects if o['type'] == 'city')
for city in cities:
    print city



json_data=open('yelp_academic_dataset_business.json')

data = json.load(json_data)
print data['business_id']

