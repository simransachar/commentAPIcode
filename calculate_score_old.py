#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'simranjitsingh'

from nltk.probability import FreqDist
from nltk.corpus import stopwords
from nltk.tokenize import SpaceTokenizer, WhitespaceTokenizer
import nltk.tag, nltk.util, nltk.stem
import re
import string
import math
from bs4 import BeautifulSoup
import csv
from decimal import *
import mysql.connector
import operator
import sys
import time
import json
import timeit

stopword_list = stopwords.words('english')
porter = nltk.PorterStemmer()
doc_frequency = {}
word_features = []
vocab_freq = {}
nDocuments = 0
# cnx = mysql.connector.connect(user='root', password='simran',
#                               host='127.0.0.1',
#                               database='comment_iq')
cnx = mysql.connector.connect(user='merrillawsdb', password='WR3QZGVaoHqNXAF',
                              host='awsdbinstance.cz5m3w6kwml8.us-east-1.rds.amazonaws.com',
                              database='comment_iq')
cursor = cnx.cursor()

json_data = open("data/vocab_freq.json")
vocab_freq = json.load(json_data)

count_read = open("data/count.txt", "r")
nDocuments = count_read.read()
nDocuments = int(nDocuments)

def NormalizeVector(vector):
    length = ComputeVectorLength(vector)
    for (k,v) in vector.items():
        if length > 0:
            vector[k] = v / length
    return vector

def ComputeVectorLength(vector):
    length = 0;
    for d in vector.values():
        length += d * d
    length = math.sqrt(length)
    return length

 # Assumes that both vectors are normalized
def ComputeCosineSimilarity(v1, v2):
	dotproduct = 0
	for (key1,val1) in v1.items():
		if key1 in v2:
			dotproduct += val1 * v2[key1]
	return dotproduct;


def CleanAndTokenize(text):
    # Strip URLs and replace with token "URLURLURL"
    r = re.compile(r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+")
    text = re.sub(r, " URLURLURL", text)
    # Strip html tags
    soup = BeautifulSoup(text)
    for tag in soup.findAll(True):
        tag.replaceWithChildren()
        text = soup.get_text()
        # Normalize everything to lower case
    text = text.lower()
    # Strip line breaks and endings \r \n
    r = re.compile(r"[\r\n]+")
    text = re.sub(r, "", text)
    table = {
        ord(u'\u2018') : u"'",
        ord(u'\u2019') : u"'",
        ord(u'\u201C') : u'"',
        ord(u'\u201d') : u'"',
        ord(u'\u2026') : u'',
        ord(u'\u2014') : u'', # get rid of em dashes
    }
    #text = text.translate(table)
    # Normalize contractions
    # e.g. can't => can not, it's => it is, he'll => he will
    text = text.replace("can't", "can not")
    text = text.replace("couldn't", "could not")
    text = text.replace("don't", "do not")
    text = text.replace("didn't", "did not")
    text = text.replace("doesn't", "does not")
    text = text.replace("shouldn't", "should not")
    text = text.replace("haven't", "have not")
    text = text.replace("aren't", "are not")
    text = text.replace("weren't", "were not")
    text = text.replace("wouldn't", "would not")
    text = text.replace("hasn't", "has not")
    text = text.replace("hadn't", "had not")
    text = text.replace("won't", "will not")
    text = text.replace("wasn't", "was not")
    text = text.replace("can't", "can not")
    text = text.replace("isn't", "is not")
    text = text.replace("ain't", "is not")
    text = text.replace("it's", "it is")
    text = text.replace("i'm", "i am")
    text = text.replace("i'm", "i am")
    text = text.replace("i've", "i have")
    text = text.replace("i'll", "i will")
    text = text.replace("i'd", "i would")
    text = text.replace("we've", "we have")
    text = text.replace("we'll", "we will")
    text = text.replace("we'd", "we would")
    text = text.replace("we're", "we are")
    text = text.replace("you've", "you have")
    text = text.replace("you'll", "you will")
    text = text.replace("you'd", "you would")
    text = text.replace("you're", "you are")
    text = text.replace("he'll", "he will")
    text = text.replace("he'd", "he would")
    text = text.replace("he's", "he has")
    text = text.replace("she'll", "she will")
    text = text.replace("she'd", "she would")
    text = text.replace("she's", "she has")
    text = text.replace("they've", "they have")
    text = text.replace("they'll", "they will")
    text = text.replace("they'd", "they would")
    text = text.replace("they're", "they are")
    text = text.replace("that'll", "that will")
    text = text.replace("that's", "that is")
    text = text.replace("there's", "there is")
    # Strip punctuation (except for a few)
    punctuations = string.punctuation # includes following characters: !"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~
    excluded_punctuations = ["$", "%"]
    for p in punctuations:
        if p not in excluded_punctuations:
            text = text.replace(p, " ")

    # Condense double spaces
    text = text.replace("  ", " ")

    # Tokenize the text
    # NOTE: Using a simple tokenizer based on spaces ...
    # Could also try a more sophisticated tokenizer if abbreviations / contractions should be conserved
    tokenizer = WhitespaceTokenizer()
    text_tokens = tokenizer.tokenize(text)

    return text_tokens

def escape_string(string):
    res = string
    res = res.replace('\\','\\\\')
    res = res.replace('\n','\\n')
    res = res.replace('\r','\\r')
    res = res.replace('\047','\134\047') # single quotes
    res = res.replace('\042','\134\042') # double quotes
    res = res.replace('\032','\134\032') # for Win32
    return res

def error_name():
    exc_type, exc_obj, exc_tb = sys.exc_info()
    msg = str(exc_type)
    error = re.split(r'[.]',msg)
    error = re.findall(r'\w+',error[1])
    error_msg = str(error[0]) + "occured in line " + str(exc_tb.tb_lineno)
    return error_msg

# Computes the vocabulary to be used for vector operations
def ComputeVocabulary():
    n = 0
    cursor.execute("select commentBody from vocab_comments")
    for row in cursor:
        n = n + 1
        if n % 100 == 0 :
            print n
        ct = CleanAndTokenize(row[0])
        ct = [w for w in ct if w not in stopword_list]
        stemmed_tokens = [porter.stem(t) for t in ct]
        for t in stemmed_tokens:
             if t not in doc_frequency:
                 doc_frequency[t] = 1
             else:
                 doc_frequency[t] = doc_frequency[t]+1

    sorted_list = sorted(doc_frequency.items(), key=operator.itemgetter(1), reverse=True)
    # find cutoff
    unigram_cutoff = 0
    json_data = {}
    out_file = open("data/vocab_freq.json","w")
    fileWriter = csv.writer(open("data/vocab91.csv", "wb"),delimiter=",")
    for (i, (word, word_freq)) in enumerate(sorted_list):
        if word_freq < 10:
            unigram_cutoff = i - 1
            break;
        row = [word.encode("utf8"), word_freq]
        json_data[word] = word_freq
        fileWriter.writerow(row)
    json.dump(json_data,out_file)
    print "unigram cutoff: " + str(unigram_cutoff)


def ComputeCommentArticleRelevance(comment_text,article_url):
    cursor.execute("select full_text from articles where articleURL = '" + article_url + "'")
    article_data = cursor.fetchall()
    if len(article_data) < 1:
        ar_score = 0.0
        return ar_score
    for data in article_data:
        article_text = data[0]
    comment_text = comment_text.strip()
    comment_text = escape_string(comment_text)
    ct = CleanAndTokenize(comment_text)
    ct = [w for w in ct if w not in stopword_list]
    comment_stemmed_tokens = [porter.stem(t) for t in ct]
    comment_stemmed_tokens_fd  = FreqDist(comment_stemmed_tokens)
    ct = CleanAndTokenize(article_text)
    ct = [w for w in ct if w not in stopword_list]
    article_stemmed_tokens = [porter.stem(t) for t in ct]
    article_stemmed_tokens_fd  = FreqDist(article_stemmed_tokens)
    # now create the feature vectors for article and comment (this is redudant for the article on every iteration)
    article_features = {}
    comment_features = {}
    # print article_stemmed_tokens
    for w in vocab_freq:
            df = vocab_freq[w]
            log_fraction = (nDocuments / df)
            if log_fraction < 1:
                log_fraction = Decimal(nDocuments) / Decimal(df)
            if w in article_stemmed_tokens:
                 article_features[w] = article_stemmed_tokens_fd[w] * math.log(log_fraction)
            else:
                 article_features[w] = 0.0
            if w in comment_stemmed_tokens:
                 comment_features[w] = comment_stemmed_tokens_fd[w] * math.log(log_fraction)
            else:
                 comment_features[w] = 0.0

    # normalize vectors
    article_features = NormalizeVector(article_features)
    comment_features = NormalizeVector(comment_features)
    comment_article_similarity = ComputeCosineSimilarity (article_features, comment_features)
    return comment_article_similarity


def ComputeCommentConversationalRelevance(comment_text,article_url):
    centroid_comment_stemmed_tokens = []
    centroid_comment_features = {}
    cursor.execute("select commentBody from comments where articleURL = '" + article_url + "' ")
    comment_data = cursor.fetchall()
    if len(comment_data) < 10:
        cr_score = 0.0
        return cr_score
    comment_list = list(zip(*comment_data)[0])
    for comment in comment_list:
                ct = CleanAndTokenize(comment)
                ct = [w for w in ct if w not in stopword_list]
                # Update and compute the centroid
                centroid_comment_stemmed_tokens.extend([porter.stem(t) for t in ct])
    centroid_comment_stemmed_tokens_fd = FreqDist(centroid_comment_stemmed_tokens)
    start = timeit.default_timer()
    for w in vocab_freq:
                log_fraction = (nDocuments / vocab_freq[w])
                if log_fraction < 1:
                    log_fraction = Decimal(nDocuments) / Decimal(vocab_freq[w])
                if w in centroid_comment_stemmed_tokens:
                    centroid_comment_features[w] = centroid_comment_stemmed_tokens_fd[w] * math.log(log_fraction)
                else:
                    centroid_comment_features[w] = 0.0
    stop = timeit.default_timer()
    print stop - start
    start = timeit.default_timer()
    for w in vocab_freq:
        pass
    stop = timeit.default_timer()
    print stop - start
    centroid_comment_features = NormalizeVector(centroid_comment_features)
    # Now compute dist to  comment
    comment_stemmed_tokens = []
    comment_features = {}
    comment_text = comment_text.strip()
    comment_text = escape_string(comment_text)
    ct = CleanAndTokenize(comment_text)
    comment_stemmed_tokens.extend([porter.stem(t) for t in ct])
    comment_stemmed_tokens_fd  = FreqDist(comment_stemmed_tokens)
    for w in vocab_freq:
                log_fraction = (nDocuments / vocab_freq[w])
                if log_fraction < 1:
                    log_fraction = Decimal(nDocuments) / Decimal(vocab_freq[w])
                if w in comment_stemmed_tokens:
                    comment_features[w] = comment_stemmed_tokens_fd[w] * math.log(log_fraction)
                else:
                    comment_features[w] = 0.0
    comment_features = NormalizeVector(comment_features)
    comment_originality = ComputeCosineSimilarity (centroid_comment_features, comment_features)
    return comment_originality

# def add_article(article_title, article_url, article_text,material_type):
#     current_time = time.strftime("%Y-%m-%d %I:%M:%S")
#     insert_query = "INSERT INTO demo_articles (pubDate, headline, articleURL, full_text, materialType, snippet)" \
#                                     " VALUES('%s', '%s', '%s', '%s', '%s', '%s')" % \
#                                     (current_time, article_title, article_url, article_text,material_type,article_text)
#     cursor.execute(insert_query)

def main(comment_text,article_url):
    ar_score = ComputeCommentArticleRelevance(comment_text,article_url)
    cr_score = ComputeCommentConversationalRelevance(comment_text,article_url)
    return (ar_score,cr_score)


