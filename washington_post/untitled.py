from flask import Flask,render_template, request, redirect, url_for, jsonify
import time
from bs4 import BeautifulSoup
import mysql.connector
import json
import requests
from ConfigParser import SafeConfigParser
from random import randint

app = Flask(__name__)
app.debug = True

# Get the config file for database
parser = SafeConfigParser()
# Edit the config file to fill in your credentials
parser.read('database.ini')

# Fetch the credentials from config file
user = parser.get('credentials', 'user')
password = parser.get('credentials', 'password')
host = parser.get('credentials', 'host')
database = parser.get('credentials', 'database')

base_url = "http://api.comment-iq.com/commentIQ/v1"

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
    cnx = mysql.connector.connect(user=user, password=password, host=host, database=database)
    cursor = cnx.cursor()
    cursor.execute("select * from client_articles")
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
    cursor.execute("select headline,articleURL,full_text from client_articles order by articleID desc limit 2")
    disp_list = cursor.fetchall()
    for row in disp_list:
        row = list(row)
        article_text = row[2]
        soup = BeautifulSoup(article_text)
        for tag in soup.findAll(True):
            tag.replaceWithChildren()
            row[2] = soup.get_text()
    cnx.close

    current_time = time.strftime("%B %d, %Y")

    return render_template('index.html',article_text_list=article_text_list,article_title=article_title, \
                           article_url=article_url,disp_list=disp_list,current_time=current_time)

@app.route('/articles')
def articles():
    article_data = []
    article_url = request.args.get('article_url')
    new_comment=request.args.get('new_comment')
    updated=request.args.get('updated')
    sort = request.args.get('sort')
    print "---------"
    print article_url

    cnx = mysql.connector.connect(user=user, password=password, host=host, database=database)
    cursor = cnx.cursor()

    cursor.execute("select headline,full_text,articleURL from client_articles where articleURL = '"+ article_url +"'")
    for row in cursor:
        article_title = row[0]
        article_text = row[1]
        article_text1 = row[1]

        soup = BeautifulSoup(row[1])
        for tag in soup.findAll(True):
            tag.replaceWithChildren()
            article_text = soup.get_text()

    article_data.extend((article_title,article_text1,article_url))
    comment_data =[]
    if sort == 'ar':
        cursor.execute("select commentBody,approveDate,display_name,ArticleRelevance,ConversationalRelevance," \
                       "commentID,PersonalXP,Readability,CommentLength from client_comments where articleURL = '" + article_url + "' "
                        "order by ArticleRelevance desc")
        new_comment="yes"
    elif sort == 'cr' :
        cursor.execute("select commentBody,approveDate,display_name,ArticleRelevance,ConversationalRelevance,commentID" \
                       ",PersonalXP,Readability,CommentLength from client_comments where articleURL = '" + article_url + "' "
                        "order by ConversationalRelevance desc")
        new_comment="yes"

    elif sort == 'px' :
        cursor.execute("select commentBody,approveDate,display_name,ArticleRelevance,ConversationalRelevance,commentID" \
                       ",PersonalXP,Readability,CommentLength from client_comments where articleURL = '" + article_url + "' "
                        "order by PersonalXP desc")
        new_comment="yes"

    elif sort == 'rd' :
        cursor.execute("select commentBody,approveDate,display_name,ArticleRelevance,ConversationalRelevance,commentID" \
                       ",PersonalXP,Readability,CommentLength from client_comments where articleURL = '" + article_url + "' "
                        "order by Readability desc")
        new_comment="yes"

    elif sort == 'len' :
        cursor.execute("select commentBody,approveDate,display_name,ArticleRelevance,ConversationalRelevance,commentID" \
                       ",PersonalXP,Readability,CommentLength from client_comments where articleURL = '" + article_url + "' "
                        "order by CommentLength desc")
        new_comment="yes"

    else:

        cursor.execute("select commentBody,approveDate,display_name,ArticleRelevance,ConversationalRelevance,commentID" \
                       ",PersonalXP,Readability,CommentLength from client_comments where articleURL = '" + article_url + "' "
                        "order by approveDate ")
    for row in cursor:
        row = list(row)
        row[1] = row[1].strftime('%B %d, %Y at %I:%M %p ')
        soup = BeautifulSoup(row[0])
        for tag in soup.findAll(True):
            tag.replaceWithChildren()
            row[0] = soup.get_text()
        comment_data.append(row)

    cursor.execute("select * from client_articles  limit 14,5")
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
    cnx.close

    current_time = time.strftime("%B %d, %Y")

    return render_template('style-demo.html',comment_data=comment_data,article_data=article_data,new_comment=new_comment \
                           ,article_text_list=article_text_list,article_title=article_title,article_url=article_url, \
                           current_time=current_time,updated=updated)

@app.route('/new_article', methods=['GET', 'POST'])
def new_article():
    cnx = mysql.connector.connect(user=user, password=password, host=host, database=database)
    cursor = cnx.cursor()

    if request.method == 'POST':
        article_title = request.form['title']
        if len(article_title) < 1:
            article_title = "No Title"
        article_text = request.form['article_text']
        if len(article_text) < 1:
            article_text = "No Text in the article"
        article_url = request.form['url']
        if len(article_url) < 1:
            article_url = "articleurl" + str(randint(1,100))

        material_type = request.form['type']
        current_time = time.strftime("%Y-%m-%d %I:%M:%S")
        url = base_url + "/addArticle"
        params = {'article_text' : article_text }
        param_json = json.dumps(params)
        response = requests.post(url, param_json)
        print response
        commentiq_article_id = response.json()['articleID']
        article_text = article_text.strip()
        article_text = escape_string(article_text)

        insert_query = "INSERT INTO client_articles (pubDate, headline, articleURL , full_text, materialType, commentiq_articleID)" \
                                    " VALUES('%s', '%s', '%s', '%s','%s', '%s')" % \
                                    (current_time, article_title, article_url , article_text,material_type,str(commentiq_article_id))
        cursor.execute(insert_query)
        return redirect(url_for('show_index'))
    cursor.execute("select * from client_articles  limit 14,5")
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
    cnx.commit()
    cnx.close

    current_time = time.strftime("%B %d, %Y")

    return render_template('new_article.html',article_text_list=article_text_list,article_title=article_title, \
                           current_time=current_time,article_url=article_url)

@app.route('/add_comment', methods=['GET', 'POST'])
def add_comment():
    if request.method == 'POST':
        article_url=request.args.get('article_url')

        cnx = mysql.connector.connect(user=user, password=password, host=host, database=database)
        cursor = cnx.cursor()

        cursor.execute("select commentiq_articleID from client_articles where articleURL = '"+ article_url +"'")
        for data in cursor:
            a_id = data[0]
        comment_text = request.form['comment_text']
        name = request.form['name'].strip()
        if not name:
            name = "Anonymous"
        current_time = time.strftime("%Y-%m-%d %H:%M:%S")
        url = base_url + "/addComment"
        params = {'articleID' : a_id, 'commentBody' : comment_text}
        param_json = json.dumps(params)
        response = requests.post(url, param_json)
        ar_score = response.json()['ArticleRelevance']
        cr_score = response.json()['ConversationalRelevance']
        PersonalXP = response.json()['PersonalXP']
        Readability = response.json()['Readability']
        Length = response.json()['Length']

        commentiq_comment_id = response.json()['commentID']
        print response.json()
        comment_text = comment_text.strip()
        comment_text = escape_string(comment_text)
        insert_query = "INSERT INTO client_comments (commentBody, approveDate, articleURL, display_name, " \
                       "ArticleRelevance,ConversationalRelevance,PersonalXP,Readability,CommentLength, commentiq_commentID) " \
                       "VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" % \
                       (comment_text,current_time,article_url,name,str(ar_score),str(cr_score),str(PersonalXP), \
                        str(Readability), str(Length),str(commentiq_comment_id))
        cursor.execute(insert_query)
        new_comment="yes"
        cnx.commit()
        cnx.close
    return redirect(url_for('articles',article_url=article_url,new_comment=new_comment))

@app.route('/edit_comment')
def edit_comment():
    article_data = []
    commentID = request.args.get('commentID')
    print commentID
    article_url = request.args.get('article_url')
    new_comment=request.args.get('new_comment')
    sort = request.args.get('sort')

    cnx = mysql.connector.connect(user=user, password=password, host=host, database=database)
    cursor = cnx.cursor()

    cursor.execute("select headline,full_text,articleURL from client_articles where articleURL = '"+ article_url +"'")
    for row in cursor:
        article_title = row[0]
        article_text = row[1]
        soup = BeautifulSoup(row[1])
        for tag in soup.findAll(True):
            tag.replaceWithChildren()
            article_text = soup.get_text()

    article_data.extend((article_title,article_text,article_url))
    comment_data =[]
    if sort == 'ar':
        cursor.execute("select commentBody,approveDate,display_name,ArticleRelevance,ConversationalRelevance," \
                       "commentID,PersonalXP,Readability,CommentLength from client_comments where articleURL = '" + article_url + "' "
                        "order by ArticleRelevance desc")
        new_comment="yes"
    elif sort == 'cr' :
        cursor.execute("select commentBody,approveDate,display_name,ArticleRelevance,ConversationalRelevance,commentID" \
                       ",PersonalXP,Readability,CommentLength from client_comments where articleURL = '" + article_url + "' "
                        "order by ConversationalRelevance desc")
        new_comment="yes"
    elif sort == 'px' :
        cursor.execute("select commentBody,approveDate,display_name,ArticleRelevance,ConversationalRelevance,commentID" \
                       ",PersonalXP,Readability,CommentLength from client_comments where articleURL = '" + article_url + "' "
                        "order by PersonalXP desc")
        new_comment="yes"

    elif sort == 'rd' :
        cursor.execute("select commentBody,approveDate,display_name,ArticleRelevance,ConversationalRelevance,commentID" \
                       ",PersonalXP,Readability,CommentLength from client_comments where articleURL = '" + article_url + "' "
                        "order by Readability desc")
        new_comment="yes"

    elif sort == 'len' :
        cursor.execute("select commentBody,approveDate,display_name,ArticleRelevance,ConversationalRelevance,commentID" \
                       ",PersonalXP,Readability,CommentLength from client_comments where articleURL = '" + article_url + "' "
                        "order by CommentLength desc")
        new_comment="yes"

    else:
        cursor.execute("select commentBody,approveDate,display_name,ArticleRelevance,ConversationalRelevance,commentID" \
                       ",PersonalXP,Readability,CommentLength from client_comments where articleURL = '" + article_url + "' "
                        "order by approveDate ")
    for row in cursor:
        row = list(row)
        row[1] = row[1].strftime('%B %d, %Y at %I:%M %p ')
        soup = BeautifulSoup(row[0])
        for tag in soup.findAll(True):
            tag.replaceWithChildren()
            row[0] = soup.get_text()
        comment_data.append(row)

    cursor.execute("select * from client_articles  limit 14,5")
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
    cnx.close

    current_time = time.strftime("%B %d, %Y")

    return render_template('edit_comment.html',comment_data=comment_data,article_data=article_data,new_comment=new_comment \
                           ,article_text_list=article_text_list,article_title=article_title,article_url=article_url, \
                           current_time=current_time,commentID=commentID)

@app.route('/update_comment', methods=['GET', 'POST'])
def update_comment():
    if request.method == 'POST':
        cnx = mysql.connector.connect(user=user, password=password, host=host, database=database)
        cursor = cnx.cursor()

        commentID = request.args.get('commentID')
        article_url = request.args.get('article_url')
        comment_text = request.form['comment_text']
        comment_text = comment_text.strip()
        cursor.execute("select commentiq_commentID from client_comments where commentID = '"+ str(commentID) +"'")
        commentiq_commentID = cursor.fetchall()[0][0]
        url = base_url + "/updateComment"
        params = {'commentBody' : comment_text, 'commentID' : commentiq_commentID }
        param_json = json.dumps(params)
        response = requests.post(url, param_json)
        ar_score = response.json()['ArticleRelevance']
        cr_score = response.json()['ConversationalRelevance']
        PersonalXP = response.json()['PersonalXP']
        Readability = response.json()['Readability']
        Length = response.json()['Length']

        print response.json()
        comment_text = escape_string(comment_text)
        comment_text = comment_text.encode('utf-8')
        update = "UPDATE client_comments SET commentBody = '"+ str(comment_text) +"'," \
                 "ArticleRelevance = '"+ str(ar_score) +"',ConversationalRelevance = '"+ str(cr_score) +"' " \
                 ",PersonalXP = '"+ str(PersonalXP) +"',Readability = '"+ str(Readability) +"'" \
                 ",CommentLength = '"+ str(Length) +"' where commentID = '"+ str(commentID) +"'"
        cursor.execute(update)
        cnx.commit()
        cnx.close
    return redirect(url_for('articles',article_url=article_url,updated=commentID))

@app.route('/delete_comment', methods=['GET', 'POST'])
def delete_comment():
    commentID = request.args.get('commentID')
    article_url = request.args.get('article_url')

    cnx = mysql.connector.connect(user=user, password=password, host=host, database=database)
    cursor = cnx.cursor()

    cursor.execute("select commentiq_commentID from client_comments where commentID = '"+ str(commentID) +"'")
    commentiq_commentID = cursor.fetchall()[0][0]
    url = base_url + "/deleteComment/" + str(commentiq_commentID) +"'"
    response = requests.get(url)
    print response.json()
    delete = "delete from client_comments where commentID = '"+ str(commentID) +"'"
    cursor.execute(delete)
    cursor.execute("select commentID from client_comments where articleURL = '"+ article_url +"' and " \
                   "commentID > '"+ commentID +"' Limit 1 ")
    next_id = cursor.fetchall()
    if len(next_id) > 0:
        next_id = next_id[0][0]
        new_comment=None
    else:
        next_id = None
        new_comment="yes"
    cnx.commit()
    cnx.close
    return redirect(url_for('articles',article_url=article_url,updated=next_id,new_comment=new_comment))

@app.route('/get_AR', methods=['GET', 'POST'])
def get_AR():
    commentID = request.args.get('commentID')
    article_url = request.args.get('article_url')

    cnx = mysql.connector.connect(user=user, password=password, host=host, database=database)
    cursor = cnx.cursor()

    cursor.execute("select commentiq_commentID from client_comments where commentID = '"+ str(commentID) +"'")
    commentiq_commentID = cursor.fetchall()[0][0]

    url = base_url + "/getArticleRelevance/" + str(commentiq_commentID) +"'"
    response = requests.get(url)
    ar_score = response.json()['ArticleRelevance']
    update = "UPDATE client_comments SET ArticleRelevance = '" + str(ar_score) + "' where commentID = '"+ str(commentID) +"'"
    cursor.execute(update)
    cnx.commit()
    cnx.close
    return redirect(url_for('articles',article_url=article_url,updated=commentID))

@app.route('/get_CR', methods=['GET', 'POST'])
def get_CR():
    commentID = request.args.get('commentID')
    article_url = request.args.get('article_url')

    cnx = mysql.connector.connect(user=user, password=password, host=host, database=database)
    cursor = cnx.cursor()

    cursor.execute("select commentiq_commentID from client_comments where commentID = '"+ str(commentID) +"'")
    commentiq_commentID = cursor.fetchall()[0][0]

    url = base_url + "/getConversationalRelevance/" + str(commentiq_commentID) +"'"

    response = requests.get(url)
    cr_score = response.json()['ConversationalRelevance']
    print response.json()
    update = "UPDATE client_comments SET ConversationalRelevance = '" + str(cr_score) + "' where commentID = '"+ str(commentID) +"'"
    cursor.execute(update)
    cnx.commit()
    cnx.close
    return redirect(url_for('articles',article_url=article_url,updated=commentID))
@app.route('/get_CR', methods=['GET', 'POST'])

@app.route('/get_PX', methods=['GET', 'POST'])
def get_PX():
    commentID = request.args.get('commentID')
    article_url = request.args.get('article_url')

    cnx = mysql.connector.connect(user=user, password=password, host=host, database=database)
    cursor = cnx.cursor()

    cursor.execute("select commentiq_commentID from client_comments where commentID = '"+ str(commentID) +"'")
    commentiq_commentID = cursor.fetchall()[0][0]

    url = base_url + "/getPersonalXP/" + str(commentiq_commentID) +"'"
    response = requests.get(url)
    PersonalXP = response.json()['PersonalXP']
    print response.json()
    update = "UPDATE client_comments SET PersonalXP = '" + str(PersonalXP) + "' where commentID = '"+ str(commentID) +"'"
    cursor.execute(update)
    cnx.commit()
    cnx.close
    return redirect(url_for('articles',article_url=article_url,updated=commentID))

@app.route('/get_RD', methods=['GET', 'POST'])
def get_RD():
    commentID = request.args.get('commentID')
    article_url = request.args.get('article_url')

    cnx = mysql.connector.connect(user=user, password=password, host=host, database=database)
    cursor = cnx.cursor()

    cursor.execute("select commentiq_commentID from client_comments where commentID = '"+ str(commentID) +"'")
    commentiq_commentID = cursor.fetchall()[0][0]

    url = base_url + "/getReadability/" + str(commentiq_commentID) +"'"
    response = requests.get(url)
    Readability = response.json()['Readability']
    print response.json()
    update = "UPDATE client_comments SET Readability = '" + str(Readability) + "' where commentID = '"+ str(commentID) +"'"
    cursor.execute(update)
    cnx.commit()
    cnx.close
    return redirect(url_for('articles',article_url=article_url,updated=commentID))

@app.route('/get_Len', methods=['GET', 'POST'])
def get_Len():
    commentID = request.args.get('commentID')
    article_url = request.args.get('article_url')

    cnx = mysql.connector.connect(user=user, password=password, host=host, database=database)
    cursor = cnx.cursor()


    cursor.execute("select commentiq_commentID from client_comments where commentID = '"+ str(commentID) +"'")
    commentiq_commentID = cursor.fetchall()[0][0]

    url = base_url + "/getLength/" + str(commentiq_commentID) +"'"
    response = requests.get(url)
    Length = response.json()['Length']
    print response.json()
    update = "UPDATE client_comments SET CommentLength = '" + str(Length) + "' where commentID = '"+ str(commentID) +"'"
    cursor.execute(update)
    cnx.commit()
    cnx.close

    return redirect(url_for('articles',article_url=article_url,updated=commentID))


@app.route('/get_AllScores', methods=['GET', 'POST'])
def get_scores():
    commentID = request.args.get('commentID')
    article_url = request.args.get('article_url')

    cnx = mysql.connector.connect(user=user, password=password, host=host, database=database)
    cursor = cnx.cursor()

    cursor.execute("select commentiq_commentID from client_comments where commentID = '"+ str(commentID) +"'")
    commentiq_commentID = cursor.fetchall()[0][0]

    url = base_url + "/getScores/" + str(commentiq_commentID) +"'"
    response = requests.get(url)
    ar_score = response.json()['ArticleRelevance']
    cr_score = response.json()['ConversationalRelevance']
    PersonalXP = response.json()['PersonalXP']
    Readability = response.json()['Readability']
    Length = response.json()['Length']

    print response.json()
    update = "UPDATE client_comments SET ArticleRelevance = '" + str(ar_score) + "', ConversationalRelevance = '" + str(cr_score) + "' " \
              ", PersonalXP = '" + str(PersonalXP) + "', Readability = '" + str(Readability) + "' " \
              ", CommentLength = '" + str(Length) + "' where commentID = '"+ str(commentID) +"'"
    cursor.execute(update)
    cnx.commit()
    cnx.close
    return redirect(url_for('articles',article_url=article_url,updated=commentID))


if __name__ == '__main__':
    app.run()
