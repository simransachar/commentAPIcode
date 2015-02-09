__author__ = 'simranjitsingh'

import json
import requests
from calculate_score import calcPersonalXPScores, calcReadability
article_text = "Sheila Heen, an expert in negotiation and difficult"

#url = "http://ec2-54-173-77-171.compute-1.amazonaws.com/update_demo_comment"
url = "http://127.0.0.1:5000/commentIQ/v1/updateComment"
#url = "http://127.0.0.1:5000/commentIQ/v1/updateArticle"
#url = "http://127.0.0.1:5000/commentIQ/v1/addArticle"
#url = "http://127.0.0.1:5000/commentIQ/v1/addComment"
#url = "http://ec2-54-173-77-171.compute-1.amazonaws.com/commentIQ/v1/addComment"
#url = "http://ec2-54-173-77-171.compute-1.amazonaws.com/commentIQ/v1/updateComment"
articleID = 78
commentID = 172
comment_text = "Oh how true - you nailed it again! In my case, viewing the entire season of Downton Abbey - accompanied by a healthy swoon - was the best anti-dote possible to having accidentally exposed myself to the first (and for me the last) season of Breaking Bad. And I admit to an ongoing crush on Mr. Bates"
#params = {'article_text' : article_text }
params = {'commentBody' : comment_text, 'commentID' : commentID }
#params = {'commentBody' : comment_text, 'articleID' : articleID }
#params = {'article_text' : comment_text, 'articleID' : articleID }
param_json = json.dumps(params)
response = requests.post(url, param_json)
# demo_article_id = response.json()['demo_article_id']
print response.json()

# r = calcPersonalXPScores(comment_text)
# print r
# r = calcReadability(comment_text)
# print r

#url = "http://ec2-54-173-77-171.compute-1.amazonaws.com/get_scores/'"+ str(commentID) +"'"
#url = "http://ec2-54-173-77-171.compute-1.amazonaws.com/get_ArticleRelevance/'"+ str(commentID) +"'"
#url = 'http://127.0.0.1:5000/delete_demo_comment/"' + `commentID` + '"'
url = "http://127.0.0.1:5000/commentIQ/v1/getScores/'"+ str(commentID) +"'"
#url = "http://ec2-54-173-77-171.compute-1.amazonaws.com/commentIQ/v1/getScores/'"+ str(commentID) +"'"
#url = "http://127.0.0.1:5000/commentIQ/v1/getConversationalRelevance/'"+ str(commentID) +"'"
#url = "http://127.0.0.1:5000/commentIQ/v1/getArticleRelevance/'"+ str(commentID) +"'"
#url = "http://127.0.0.1:5000/commentIQ/v1/getPersonalXP/'"+ str(commentID) +"'"
#url = "http://127.0.0.1:5000/commentIQ/v1/deleteComment/'"+ str(commentID) +"'"
#url = "http://127.0.0.1:5000/commentIQ/v1/getReadability/'"+ str(commentID) +"'"
response = requests.get(url)
print response.json()