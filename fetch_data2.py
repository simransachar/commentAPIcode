__author__ = 'ssachar'

import mysql.connector

# cnx = mysql.connector.connect(user='merrillawsdb', password='WR3QZGVaoHqNXAF',
#                              host='awsdbinstance.cz5m3w6kwml8.us-east-1.rds.amazonaws.com',
#                              database='comment_iq')

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

cursor.execute("DESCRIBE articles")

for i in cursor:
    print i


cursor.execute("select * from articles")
data = cursor.fetchall()

for row in data:
    article_title = row[2]
    article_text = row[5]
    article_url = row[7]
    material_type = row[3]
    current_time = row[1]
    article_text = article_text.strip()
    article_text = escape_string(article_text)
    # update = "UPDATE demo_articles set headline = '"+ article_title +"' where articleID = '"+ str(row[6]) +"'"
    # cursor.execute(update)
    insert_query1 = "INSERT INTO demo_articles (pubDate, full_text)" \
                                    " VALUES('%s', '%s')" % \
                                    (current_time, article_text)
#    cursor.execute(insert_query1)
#    demo_article_id = cursor.lastrowid

    # insert_query2 = "INSERT INTO articles (pubDate, headline, articleURL, full_text, materialType, snippet, demo_articleID)" \
    #                                 " VALUES('%s', '%s', '%s', '%s', '%s', '%s', '%d')" % \
    #                                 (current_time, article_title, article_url, article_text,material_type,article_text, demo_article_id)
    # cursor.execute(insert_query2)
#    update_query = "UPDATE articles set demo_articleID = '"+ str(demo_article_id) +"' where articleID = '"+ str(row[0]) +"'"
#    cursor.execute(update_query)



#cnx.commit()



cnx.close