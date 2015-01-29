__author__ = 'simranjitsingh'

import json
import requests
article_text = "Sheila Heen, an expert in negotiation and difficult"

#url = "http://ec2-54-173-77-171.compute-1.amazonaws.com/update_demo_comment"
url = "http://127.0.0.1:5000/update_demo_comment"
#articleID = 77
commentID = 1889999999999
comment_text = "Oh how true - you nailed it again! In my case, viewing the entire season of Downton Abbey - accompanied by a healthy swoon - was the best anti-dote possible to having accidentally exposed myself to the first (and for me the last) season of Breaking Bad. And I admit to an ongoing crush on Mr. Bates"
#params = {'article_text' : article_text }
params = {'comment_text' : comment_text, 'comment_id' : commentID }
param_json = json.dumps(params)
response = requests.post(url, param_json)
# demo_article_id = response.json()['demo_article_id']
print response.json()


#url = "http://ec2-54-173-77-171.compute-1.amazonaws.com/delete_demo_comment/'"+ demo_commentID +"'"
#url = 'http://127.0.0.1:5000/delete_demo_comment/"' + `commentID` + '"'
url = "http://127.0.0.1:5000/delete_demo_comment/'"+ str(commentID) +"'"
print url


response = requests.get(url)
print response.json()