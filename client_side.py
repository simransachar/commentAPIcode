__author__ = 'simranjitsingh'

from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
import time
from bs4 import BeautifulSoup
import calculate_score
import mysql.connector

app = Flask(__name__)
app.debug = True

cnx = mysql.connector.connect(user='root', password='simran',
                              host='127.0.0.1',
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
    cursor.execute("select * from articles")
    disp_list = cursor.fetchall()
    return render_template('index2.html',disp_list=disp_list)

@app.route('/article_details')
def article_details():
    article_data = []
    article_url=request.args.get('article_url')
    new_comment=request.args.get('new_comment')
    print article_url
    cursor.execute("select headline,full_text from articles where articleURL = '"+ article_url +"'")
    for row in cursor:
        article_title = row[0]
        article_text = row[1]
        soup = BeautifulSoup(row[1])
        for tag in soup.findAll(True):
            tag.replaceWithChildren()
            article_text = soup.get_text()

    article_data.extend((article_title,article_text,article_url))
    comment_data =[]
    cursor.execute("select commentBody,ar_score,cr_score from comments where articleURL = '" + article_url + "' order by approveDate ")
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
        article_url = request.form['url']
        material_type = request.form['type']
        current_time = time.strftime("%Y-%m-%d %I:%M:%S")
        article_text = article_text.strip()
        article_text = escape_string(article_text)
        insert_query = "INSERT INTO articles (pubDate, headline, articleURL, full_text, materialType, snippet)" \
                                    " VALUES('%s', '%s', '%s', '%s', '%s', '%s')" % \
                                    (current_time, article_title, article_url, article_text,material_type,article_text)
        cursor.execute(insert_query)
        calculate_score.add_article(article_title, article_url, article_text,material_type)
        return redirect(url_for('show_index'))
    return render_template('add_article.html')

@app.route('/add_comment', methods=['GET', 'POST'])
def add_comment():
    if request.method == 'POST':
        article_url=request.args.get('article_url')
        comment_text = request.form['comment_text']
        current_time = time.strftime("%Y-%m-%d %I:%M:%S")
        ar_score, cr_score = calculate_score.main(comment_text,article_url)
        comment_text = comment_text.strip()
        comment_text = escape_string(comment_text)
        insert_query = "INSERT INTO comments (commentBody, approveDate, articleURL,ar_score,cr_score) " \
                       "VALUES ('%s','%s','%s','%s','%s')" % \
                       (comment_text,current_time,article_url,str(ar_score),str(cr_score))
        cursor.execute(insert_query)
        new_comment="yes"
    return redirect(url_for('article_details',article_url=article_url,new_comment=new_comment))

if __name__ == '__main__':
    app.run()

