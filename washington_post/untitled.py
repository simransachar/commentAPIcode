from flask import Flask,render_template, request, redirect, url_for, jsonify
import time
from bs4 import BeautifulSoup
import mysql.connector
import json
import requests

app = Flask(__name__)
app.debug = True

cnx = mysql.connector.connect(user='root', password='simran',
                              host='127.0.0.1',
                              database='comment_iq')
# cnx = mysql.connector.connect(user='merrillawsdb', password='WR3QZGVaoHqNXAF',
#                              host='awsdbinstance.cz5m3w6kwml8.us-east-1.rds.amazonaws.com',
#                              database='comment_iq')
cursor = cnx.cursor()

def escape_string(string):
    res = string
    res = res.replace('\\','\\\\')
    res = res.replace('\n','\\n')
    res = res.replace('\r','\\r')
    res = res.replace('\047','\134\047') # single quotes
    res = res.replace('\042','\134\042') # double quotes
    res = res.replace('\032','\134\032') # for Win32
    return res

@app.route('/')
def hello_world():
    cursor.execute("select * from articles")
    article_text_list = []
    article_title = []
    article_url = []
    disp_list = cursor.fetchall()
    for row in disp_list:
        article_text = row[5]
        soup = BeautifulSoup(article_text)
        for tag in soup.findAll(True):
            tag.replaceWithChildren()
            article_text = soup.get_text()
        article_text_list.append(article_text)
        article_title.append(row[2])
        article_url.append(row[7])
    return render_template('index.html',article_text_list=article_text_list,article_title=article_title,article_url=article_url)

@app.route('/articles')
def articles():
    article_data = []
    article_url = request.args.get('article_url')
    new_comment=request.args.get('new_comment')
    cursor.execute("select headline,full_text,articleURL from articles where articleURL = '"+ article_url +"'")
    for row in cursor:
        article_title = row[0]
        article_text = row[1]
        soup = BeautifulSoup(row[1])
        for tag in soup.findAll(True):
            tag.replaceWithChildren()
            article_text = soup.get_text()

    article_data.extend((article_title,article_text,article_url))
    comment_data =[]
    cursor.execute("select commentBody,approveDate,display_name,ar_score,cr_score from comments where articleURL = '" + article_url + "' order by approveDate ")
    for row in cursor:
        row = list(row)
        row[1] = row[1].strftime('%B %d, %Y at %I:%M %p ')
        soup = BeautifulSoup(row[0])
        for tag in soup.findAll(True):
            tag.replaceWithChildren()
            row[0] = soup.get_text()
        comment_data.append(row)

    cursor.execute("select * from articles  limit 14,5")
    article_text_list = []
    article_title = []
    article_url = []
    disp_list = cursor.fetchall()
    for row in disp_list:
        article_text = row[5]
        soup = BeautifulSoup(article_text)
        for tag in soup.findAll(True):
            tag.replaceWithChildren()
            article_text = soup.get_text()
        article_text_list.append(article_text)
        article_title.append(row[2])
        article_url.append(row[7])
    return render_template('style-demo.html',comment_data=comment_data,article_data=article_data,new_comment=new_comment \
                           ,article_text_list=article_text_list,article_title=article_title,article_url=article_url)


@app.route('/add_comment', methods=['GET', 'POST'])
def add_comment():
    if request.method == 'POST':
        article_url=request.args.get('article_url')
        cursor.execute("select demo_articleID from articles where articleURL = '"+ article_url +"'")
        for data in cursor:
            a_id = data[0]
        comment_text = request.form['comment_text']
        name = request.form['name'].strip()
        if not name:
            name = "Anonymous"
        current_time = time.strftime("%Y-%m-%d %H:%M:%S")
        url = "http://ec2-54-173-77-171.compute-1.amazonaws.com/get_scores"
        params = {'article_id' : a_id, 'comment_text' : comment_text}
        param_json = json.dumps(params)
        response = requests.post(url, param_json)
        ar_score = response.json()['ar_score']
        cr_score = response.json()['cr_score']
        demo_comment_id = response.json()['demo_comment_id']
        comment_text = comment_text.strip()
        comment_text = escape_string(comment_text)
        insert_query = "INSERT INTO comments (commentBody, approveDate, articleURL, display_name, ar_score,cr_score, demo_commentID) " \
                       "VALUES ('%s','%s','%s','%s','%s','%s','%s')" % \
                       (comment_text,current_time,article_url,name,str(ar_score),str(cr_score), str(demo_comment_id))
        cursor.execute(insert_query)
        new_comment="yes"
    return redirect(url_for('articles',article_url=article_url,new_comment=new_comment))


if __name__ == '__main__':
    app.run()
