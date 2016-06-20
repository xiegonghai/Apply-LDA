# -*- coding: utf-8 -*-
import sys, os, re, random, math, urllib2, time, cPickle
import numpy
#following packet use for clound_pic 
import onlineldavb
import sys
import time
reload(sys)
sys.setdefaultencoding('utf-8')
##################################################################################################################################
basic_path = '/home/xxmonitor/xxmonitor/topic_txts/news_lda'
def create_dir():   
    save_dir_txt= 'topic_txt_'+sys.argv[1]
    save_dir_php = basic_path+'/topic_'+sys.argv[1]
    if not os.path.exists(save_dir_txt):
        print "++++++++++++++++create dir: "+save_dir_txt+"+++++++++++++++++++"
        os.mkdir(save_dir_txt)
    if not os.path.exists(save_dir_php):
        print "++++++++++++++++create dir: "+save_dir_php+"+++++++++++++++++++"
        os.mkdir(save_dir_php)
##################################################################################################################################
def save_topics(argv1):
    """
    Displays topics fit by onlineldavb.py. The first column gives the
    (expected) most prominent words in the topics, the second column
    gives their (expected) relative prominence.
    """
    stop = 'chineseNoStopWords.txt'
    #argv2 = 'lambda-500.dat'
    vocab = str.split(file(stop).read())
    testlambda = numpy.loadtxt(argv1)
    topic_list_txt = 'topic_txt_'+sys.argv[1]+'/topics_list_'+sys.argv[1]+'.txt'
    topic_php = basic_path+'/topic_'+sys.argv[1]
    ftopic = open(topic_list_txt,'w')
    for k in range(0,len(testlambda)):
        lambdak = list(testlambda[k, :])
        lambdak = lambdak / sum(lambdak)
        temp = zip(lambdak, range(0, len(lambdak))) #one corresponding  one
        temp = sorted(temp, key = lambda x: x[0], reverse=True)
        print 'topic %d:' % (k)
        # feel free to change the "53" here to whatever fits your screen nicely.
        line = ''
        num = ''
        if k <9:
            num = '0'+str(k+1)
        else:
            num = str(k+1)
        now_php = topic_php+'/'+'topic_'+num+'.php'
        fphp = open(now_php,'w')
        php_con = '<?php\n    $tags = array(\n'
        for i in range(0,200):
            print '%20s  \t---\t  %.4f' % (vocab[temp[i][1]], temp[i][0])
            l = '%s %.4f ' % (vocab[temp[i][1]], temp[i][0])
            php_l =' '*8+"'%s' => '%.4f',\n" % (vocab[temp[i][1]],temp[i][0])
            line = line + l
            php_con = php_con + php_l
        fphp.write(php_con+');') 
        fphp.close()
        ftopic.write(line+'\n')
        topic_name = 'topic%s' % str((k+1))
    ftopic.close()
if __name__ == '__main__':
    create_dir()
    while 1:
        try:
            last_lambda_path = 'last_lambda_'+sys.argv[1]+'.txt'
            lambda_name = file(last_lambda_path).read()
            break
        except:
            print 'not found'
            time.sleep(10)
    print lambda_name
    save_topics(lambda_name)
