CommentIQ API Code
========
Get the code up and running on your machine in 5 steps :-                                             

1. Installing the required packages
2. Get the database and table structure
3. Edit the config files
4. Collect comments data from New York Times to get the vocabulary that is used for text analysis calculations
5. Run the CommentIQ API code


### 1. Installing the required packages

Please install the following softwares/packages before proceeding to step2

* Python 2.7
* Apache server (or any other server to run flask)
* flask
* NLTK
* NLTK corpus for 'stop words' 
* MySQL
* MySQL Python connector
* BeautifulSoup(bs4)
* ConfigParser (if not included in default python libraries)


### 2. Get the database and table structure

The structures for all database tables is present in a self contained SQL file - TableStructures.sql in the 'apidata' folder. The table structures need to be ready in order to run step 4.                 
The TableStructures.sql can be imported in your database and executed to create all the table skeletons.                               
Follow the <a href="http://www.cyberciti.biz/faq/import-mysql-dumpfile-sql-datafile-into-my-database/" target="_blank">instructions</a> to import a MySQL Database.
### 3. Edit the config files

There are two config files that need to be changed in order to run steps 4 and 5.
#### 1) database.ini
```sh
[credentials]
user=
password=
host=
database=
```
Edit the database.ini file and fill in your credentials for your MySQL database connection
#### example
```sh
[credentials]
user=john
password=nash
host=127.0.0.1
database=comment_iq
```
#### 2) keys_config.ini
```sh
[API-KEYS]
KEY1=
KEY2=
```
Edit the keys_config.ini file and fill in your <b>NYT API</b> key(s)           
(Since we need to gather comment data from NYT, we need NYT API key(s) )               
Request for the NYT API keys <a href="http://developer.nytimes.com/docs/reference/keys" target="_blank">here</a>
#### example
```sh
KEY1=cksdh4934dkhf:0:2091
KEY2=cksdh4934dkhf:0:2092
```
### 4. Collect comments data from New York Times to get the vocabulary that is used for text analysis calculations
In order to run the API code we need to create vocabulary which are uni-grams that occurred 10 or more times across all comments in the database. This cocabulary is used to define a feature vector to describe each comment and article. It is advisable to get fair amount of data like 3-6 months worth of comments in order to get more accurate results. You might also consider updating your vocabulary periodically so that new words that are introduced in a news discourse can be accounted for. 
####
Python script to perform this operation : NytApiCall_ComputeVocab.py
####Steps to Run NytApiCall_ComputeVocab.py :

* Change the COMMUNITY_API_KEY_LIST in the code according to the number of keys you have. 
* Make sure the Key-Value pair in the code and keys_config.ini file are in sync.
* Each NYT API keys have a limit of 5000 calls per day. So please make sure the key limit does not exceed more than 5000.

The Code perform 3 operations :

1) <b>CollectComments()</b> :                    
* Upon running NytApiCall_ComputeVocab.py it will ask the user to enter start and end date. 
* This function will collect all the comments data from the New York Times as per the mentioned dates. 
* The comments data will be stored in the vocab_comments table. 
* The offset value is 25 which means each call will fetch 25 comments. 
* The user can also decrease the key_limit value if desired to run a small cycle.

2) <b>ComputeVocabulary() </b> : Get the frequency distribution of each word across all comments in the vocab_comments table and store in a JSON (vocab_freq.json).

3) <b> getDocumentCount() </b> : Count the number of comments in the vocab_comments table and store in a JSON(document_count.json) which will be later used to calculate feature vector.


###5.Run the CommentIQ API code
The python-flask code : CommentIQ_API.py uses the subroutine - calculate_score.py and its functions to perform the calculations of all the four criteria. Look for in-line comments in order to understand the complete code.

run the code
```sh 
>>> python CommentIQ_API.py 
```
This will start the flask server and you can start using the CommentIQ API.

<b>Note: </b>For the local machine the base url will change according to your host name. For example most local machines will have local server running on 127.0.0.1:5000.  In this case the base url will be : http://127.0.0.1:5000/commentIQ/v1
#####
###  Example
##### Python Code
```sh
import requests
import json

your_comment_text = "Your Comment Text"
articleID = 78
url = "http://127.0.0.1:5000/commentIQ/v1/addComment"
params = {'commentBody' : your_comment_text, 'articleID' : articleID }
param_json = json.dumps(params)
response = requests.post(url, param_json)
AR = response.json()['ArticleRelevance']
CR = response.json()['ConversationalRelevance']
personal_exp = response.json()['PersonalXP']
readability = response.json()['Readability']
brevity = response.json()['Brevity']
commentID = response.json()['CommentID']
status = response.json()['status']
```
##### RESPONSE JSON
```sh
{
    "ArticleRelevance": "0.06496080742983745"
    "ConversationalRelevance": "0.4046152704799379"
    "Readability": "0.0727272727273"
    "PersonalXP": "17.2"
    "Brevity": "55"
    "status": "Insert Successful"
    "CommentID": "1714"
}        
```

In order to understand how the CommentIQ API works refer <a href="https://github.com/comp-journalism/commentIQ" target="_blank">this</a> link



