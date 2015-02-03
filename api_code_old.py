__author__ = 'ssachar'

from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash, jsonify
import time
from bs4 import BeautifulSoup
import calculate_score
import mysql.connector
import json
from mysql.connector.errors import Error

app = Flask(__name__)
app.debug = True

cnx = mysql.connector.connect(user='merrillawsdb', password='WR3QZGVaoHqNXAF',
                             host='awsdbinstance.cz5m3w6kwml8.us-east-1.rds.amazonaws.com',
                             database='comment_iq')
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
def show_index():
    article_titles = []
    article_ids = []
    cursor.execute("select articleID,full_text from demo_articles")
    for row in cursor:
	    article_ids.append(row[0])
	    article_titles.append(row[1][1:50])
    return render_template('index.html',article_ids=article_ids,article_titles=article_titles)

@app.route('/article_details')
def article_details():
    article_data = []
    article_id=request.args.get('article_id')
    new_comment=request.args.get('new_comment')
    cursor.execute("select headline,full_text from demo_articles where articleID = '"+ str(article_id) +"'")
    for row in cursor:
        article_title = row[0]
        article_text = row[1]
        soup = BeautifulSoup(row[1])
        for tag in soup.findAll(True):
            tag.replaceWithChildren()
            article_text = soup.get_text()

    article_data.extend((article_title,article_text,article_id))
    comment_data =[]
    cursor.execute("select commentBody,ar_score,cr_score from demo_comments where articleID = '" + str(article_id) + "' order by approveDate ")
    for row in cursor:
        row = list(row)
        soup = BeautifulSoup(row[0])
        for tag in soup.findAll(True):
            tag.replaceWithChildren()
            row[0] = soup.get_text()
        comment_data.append(row)

    return render_template('article_comments.html',comment_data=comment_data,article_data=article_data,new_comment=new_comment)

@app.route('/add_article', methods=['GET', 'POST'])
def add_article():
    if request.method == 'POST':
        article_title = request.form['title']
        article_text = request.form['article_text']
        material_type = request.form['type']
        current_time = time.strftime("%Y-%m-%d %I:%M:%S")
        article_text = article_text.strip()
        article_text = escape_string(article_text)
        insert_query = "INSERT INTO demo_articles (pubDate, headline, full_text, materialType, snippet)" \
                                    " VALUES('%s', '%s', '%s', '%s', '%s')" % \
                                    (current_time, article_title, article_text,material_type,article_text)
        cursor.execute(insert_query)
        # process_comments_api.add_article(article_title, article_url, article_text,material_type)
        return redirect(url_for('show_index'))

    return render_template('add_article.html')

@app.route('/add_comment', methods=['GET', 'POST'])
def add_comment():
    if request.method == 'POST':
        article_id=request.args.get('article_id')
        comment_text = request.form['comment_text']
        current_time = time.strftime("%Y-%m-%d %I:%M:%S")
        ar_score, cr_score = calculate_score.main(comment_text,article_id)
        comment_text = comment_text.strip()
        comment_text = escape_string(comment_text)
        insert_query = "INSERT INTO demo_comments (commentBody, approveDate, articleID,ar_score,cr_score) " \
                       "VALUES ('%s','%s','%s','%s','%s')" % \
                       (comment_text,current_time,article_id,str(ar_score),str(cr_score))
        cursor.execute(insert_query)

        new_comment="yes"
    return redirect(url_for('article_details',article_id=article_id,new_comment=new_comment))

@app.route('/add_demo_comment', methods=['GET', 'POST'])
def add_demo_comment():
    if request.method == 'POST':
        data = request.data
        dataDict = json.loads(data)
        article_id = dataDict['article_id']
        comment_text = dataDict['comment_text']
        comment_text = comment_text.strip()
        comment_text = escape_string(comment_text)
        current_time = time.strftime("%Y-%m-%d %I:%M:%S")
        cursor.execute("select count(*) from demo_articles where articleID = '"+ str(article_id) +"' ")
        count = cursor.fetchall()[0][0]
        if count < 1 :
            return jsonify(ar_score = 0.0, cr_score = 0.0 , demo_comment_id = None , status = "Operation failed")
        else:
            ar_score, cr_score = calculate_score.addComment(comment_text,article_id)
            insert_query = "INSERT INTO demo_comments (commentBody, approveDate, articleID,ar_score,cr_score) " \
                           "VALUES ('%s','%s','%s','%s','%s')" % \
                           (comment_text,current_time,article_id,str(ar_score),str(cr_score))
            cursor.execute(insert_query)
            demo_comment_id = cursor.lastrowid
#           cnx.commit()
            rowsaffected = cursor.rowcount
            if rowsaffected == 1:
                status = "Insert Successful"
            else:
                status = "Insert failed"
    return jsonify(ar_score = ar_score, cr_score = cr_score, demo_comment_id = demo_comment_id,status=status)

@app.route('/add_demo_article', methods=['GET', 'POST'])
def add_demo_article():
    if request.method == 'POST':
        current_time = time.strftime("%Y-%m-%d %I:%M:%S")
        data = request.data
        dataDict = json.loads(data)
        article_text = dataDict['article_text']
        article_text = article_text.strip()
        article_text = escape_string(article_text)
        insert_query = "INSERT INTO demo_articles (pubDate, full_text)" \
                                    " VALUES('%s', '%s')" % \
                                    (current_time, article_text)
        cursor.execute(insert_query)
        demo_article_id = cursor.lastrowid
        rowsaffected = cursor.rowcount
        if rowsaffected == 1:
            status = "Update Successful"
        else:
            status = "No update performed"

        return jsonify(demo_article_id = demo_article_id,status = status)

@app.route('/update_demo_comment', methods=['GET', 'POST'])
def update_demo_comment():
    if request.method == 'POST':
        data = request.data
        dataDict = json.loads(data)
        comment_id = dataDict['comment_id']
        comment_text = dataDict['comment_text']
        comment_text = comment_text.strip()
        comment_text = escape_string(comment_text)
        ar_score, cr_score = calculate_score.updateComment(comment_text,comment_id)
        update = "update demo_comments set ar_score = '"+ str(ar_score) +"', cr_score = '"+ str(cr_score) +"' , " \
                 "CommentBody = '" + comment_text + "' where commentID = '"+ str(comment_id) +"' "
        cursor.execute(update)
        rowsaffected = cursor.rowcount
        if rowsaffected == 1:
            status = "Update Successful"
        else:
            status = "No update performed"

    return jsonify(ar_score = ar_score, cr_score = cr_score, status = status)

@app.route('/delete_demo_comment/<commentID>',methods=['GET'])
def delete_demo_comment(commentID):
    if isinstance(commentID, int):
        commentID = str(commentID)
    commentID = commentID.replace("'", '')
    commentID = commentID.replace('"', '')
    delete = "delete from demo_comments where commentID = '"+ commentID +"'"
    cursor.execute(delete)
    rowsaffected = cursor.rowcount
    if rowsaffected == 1:
        status = "success"
    else:
        status = "operation failed"
    return jsonify(status = status)

@app.route('/get_ArticleRelevance/<commentID>',methods=['GET'])
def get_ar(commentID):
    if isinstance(commentID, int):
        commentID = str(commentID)
    commentID = commentID.replace("'", '')
    commentID = commentID.replace('"', '')
    cursor.execute("select ar_score from demo_comments where commentID = '" + commentID + "' ")
    scores = cursor.fetchall()
    rowsaffected = cursor.rowcount
    if rowsaffected == 1:
        status = "success"
        ar_score = scores[0][0]
    else:
        status = "operation failed"
        ar_score = 0.0
    return jsonify(ArticleRelevance = ar_score, status = status)

@app.route('/get_ConversationalRelevance/<commentID>',methods=['GET'])
def get_cr(commentID):
    if isinstance(commentID, int):
        commentID = str(commentID)
    commentID = commentID.replace("'", '')
    commentID = commentID.replace('"', '')
    cursor.execute("select cr_score from demo_comments where commentID = '" + commentID + "' ")
    scores = cursor.fetchall()
    rowsaffected = cursor.rowcount
    if rowsaffected == 1:
        status = "success"
        cr_score = scores[0][0]
    else:
        status = "operation failed"
        cr_score = 0.0
    return jsonify(ConversationalRelevance = cr_score, status = status)

@app.route('/get_scores/<commentID>',methods=['GET'])
def get_scores(commentID):
    if isinstance(commentID, int):
        commentID = str(commentID)
    commentID = commentID.replace("'", '')
    commentID = commentID.replace('"', '')
    cursor.execute("select ar_score,cr_score from demo_comments where commentID = '" + commentID + "' ")
    scores = cursor.fetchall()
    rowsaffected = cursor.rowcount
    if rowsaffected == 1:
        status = "success"
        ar_score = scores[0][0]
        cr_score = scores[0][1]
    else:
        status = "operation failed"
        ar_score = 0.0
        cr_score = 0.0
    return jsonify(ArticleRelevance = ar_score, ConversationalRelevance = cr_score, status = status)


if __name__ == '__main__':
    app.run()

