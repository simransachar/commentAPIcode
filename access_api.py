__author__ = 'simranjitsingh'

import json
import requests
article_text = "Sheila Heen, an expert in negotiation and difficult"

url = "http://ec2-54-173-77-171.compute-1.amazonaws.com/add_demo_article"
params = {'article_text' : article_text }
param_json = json.dumps(params)
response = requests.post(url, param_json)
demo_article_id = response.json()['demo_article_id']
print demo_article_id
