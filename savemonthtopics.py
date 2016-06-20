# -*- coding: utf-8 -*-
import sys
import os
import datetime
reload(sys)
sys.setdefaultencoding('utf-8')
##################################################################################################################################
news_basic_path = '/home/xxmonitor/xxmonitor/topic_txts/news_lda'
feedback_basic_path = '/home/xxmonitor/xxmonitor/topic_txts/ios_feedback_lda'
nowtime = datetime.datetime.now()
if nowtime.month==1:
	month = 12
	year = nowtime.year-1
else:
	month = nowtime.month-1
	year = nowtime.month
lastmonth = datetime.datetime(year,month,nowtime.day,0,0,0)
nowdate = lastmonth.strftime("%Y%m")
nowdate1 = nowtime.strftime("%Y%m%d")
def create_dir(day):   
    global news_basic_path
    global feedback_basic_path
    global nowdate
    global nowdate1
    if nowdate1[-2:]==day:
        os.chdir(news_basic_path)
        if not os.path.exists(nowdate):
            print "++++++++++++++++create dir: "+nowdate+"+++++++++++++++++++"
            os.mkdir(nowdate)
        os.chdir(feedback_basic_path)
        if not os.path.exists(nowdate):
            print "++++++++++++++++create dir: "+nowdate+"+++++++++++++++++++"
            os.mkdir(nowdate)
    return True
##################################################################################################################################
def save_topics():
    global news_basic_path
    global feedback_basic_path
    news_nowpath = news_basic_path+"/topic_10"
    monthnews = news_basic_path+"/"+nowdate
    news_list = os.listdir(news_nowpath)
    os.chdir(news_nowpath)
    for news in news_list:
        os.system('cp "%s" "%s" '%(news,monthnews))
    feedback_nowpath = feedback_basic_path+"/topic_10"
    monthfeedback = feedback_basic_path+"/"+nowdate
    feedback_list = os.listdir(feedback_nowpath)
    os.chdir(feedback_nowpath)
    for feedback in feedback_list:
        os.system('cp "%s" "%s" '%(feedback,monthfeedback))
    print "save succeed!!"
if __name__ == '__main__':
    create_dir('04')
    if nowdate1[-2:]=='04':
        save_topics()
