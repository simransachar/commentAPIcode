#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__ = 'simranjitsingh'

import csv

import re

def escape_string(string):
    res = string

    res = res.replace('\\\\','\\')
    res = res.replace('\\n','\n')
    res = res.replace('\\r','\r')
    res = res.replace('\134\047','\047') # single quotes
    res = res.replace('\134\042','\042') # double quotes
    res = res.replace('\134\032','\032') # for Win32
    return res

csvFile1 = open("article1_final_normalized.csv", 'rb')
csvReader1 = csv.reader(csvFile1, delimiter=',', quotechar='"')

fileWriter = csv.writer(open("article1.csv", "wb"),delimiter=",")

for row in csvReader1:
    row[2] = escape_string(row[2])
    row[2] = row[2].encode("ascii", "ignore")
    print row[2]

    fileWriter.writerow(row)

a = """Chalk up another one for the Obama administration. An excellent speech totally along Obama\'s own lines of trying to be even-handed and fair to all.
They are the first group called because that\'s their job.  They aren\'t performing charity.  If they dont like it, they should quit.  We hope that when they do come they won\'t shoot unarmed citizens, needlessly paralyze folks, or lie to cover anything up. Fingers crossed.
The FBI has much to repent for in terms of racial injustice. The Agency with Hoover at the helm relentlessly harassed Martin Luther King and his family with the goal of destroying his reputation and breaking up his family. There are many historians who believe that Hoover was hoping that Dr.King would crumble under the emotional pressure and commit suicide. It is also documented that Hoover assigned FBI agents to stalk Black students that were attending white colleges and that this policy continued well into the 70\'s.The FBI had agents infiltrate groups dedicated to nonviolent protest against immoral and unconstitutional laws and these agents were in general instructed to find a way to turn the peaceful organization into a violent one and to introduce and escalate the  violence whenever possible. In many cases this meant providing the organization with weapons even when no weapons were requested. If Mr. Comey wants to change the culture in his agency he can start with acknowledging all the damage his agency has done to the cause of racial equality(No government building should be named for J.Edgar Hoover for example). There is also a significant dearth of African American FBI agents and that  can and must be remedied immediately.
As a social scientist, I appreciate Mr. Comey’s references to research, his regular use of “often” instead of “always” (or an implied “always”) in trying to make general statements about officers, and his attempt to identify environmental influences on officers’ behaviors. Officers who regularly racially profile or work from stereotypes and hurt innocent individuals should not be excused, but to just say they’re racist is often an incomplete explanation. Mr. Comey tries to offer a more complete explanation.<br/><br/>But to say “that all people have unconscious racial biases” is not necessarily true. Research is based on sampling and averages, so it’s hard to say for sure whether it’s “all” people. But the point about biases sometimes being unconscious is important. Non-prejudiced people are often those who adjust, inhibit, or ignore their initial unconscious reactions to an outgroup member.
I began teaching at the birth of Sesame Street. I taught, \"the policeman is a person in our neighborhood...a person that you meet each day\"..  He was one to be trusted.  The one you could go to when troubled. He would even show his appearance in the classroom and explain his duties to the public.  What has happened between time???
Simply the best speech on race relations by a white politician since Abraham Lincoln !"""


r = re.findall(r'\"(.+?)\"',a)
print r