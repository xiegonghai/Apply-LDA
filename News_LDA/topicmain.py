# -*- coding: utf-8 -*-
import MySQLdb
import time
import datetime
import sys
import codecs
import printtopics
reload(sys)
sys.setdefaultencoding('utf-8')
##################################################################
import cPickle, string, numpy, getopt, sys, random, time, re, pprint
import os
import onlineldavb
import jieba
from bs4 import BeautifulSoup
DATABASE = {
    'host' : 'localhost',
    'user' : 'xxmonitor',
    'passwd' : 'access101xxmonitor!@#',
    'port' : 3306,
    'db' : 'xxmonitor_database',
}
table_name = 'xxmonitor_news_table'
db = MySQLdb.connect(host=DATABASE['host'],user=DATABASE['user'],passwd=DATABASE['passwd'],db=DATABASE['db'],port=DATABASE['port'],charset='utf8')
cursor = db.cursor(MySQLdb.cursors.DictCursor)
news_list = []
chinese_list = []
doc_list = []
stopwords_dict = {}
D = 0
last_gamma_file = ''
nowtime = datetime.datetime.now()
timestamp = nowtime + datetime.timedelta(days=-30)
keepdate = timestamp.strftime("%Y-%m-%d") 
##################################################################################################################################
def read_news():
    global table_name
    global news_list
    global db
    global D
    news_list = []
    today_table = table_name #+ time.strftime("_%Y%m%d",time.localtime())
    sql = "SELECT * FROM %s WHERE substr(date,1,10)>%s" % (table_name,keepdate)
    cursor.execute(sql);
    records = cursor.fetchall()
    D = len(records)
    i = 0 
    for r in records:
        i = i+1
        #if i>500:
        #    break
        row=r['news_detail']
        news_list.append(row) 
    db.close()
##################################################################################################################################
def preprocessing():
    read_news()
    global news_list
    global chinese_list
    chinese_list = []
    for row in news_list:
        doc_soup = BeautifulSoup(row,'lxml')
        doc = []
        for p in doc_soup.find_all('p'):
            line = re.findall(ur"[\u4e00-\u9fa5]",p.text,re.MULTILINE)
            line = ''.join(line)
            doc.append(line)
        doc = ','.join(doc)
        chinese_list.append(doc)
##################################################################################################################################
def load_stopwords():
    global stopwords_dict
    f = file('./chinese_stopwords_utf8.txt').readlines()
    i = 0
    for one in f:
        print one+"============="
        one = one.replace('\r\n','')
        stopwords_dict[one] = i
        i = i+1
    #print stopwords_dict
##################################################################################################################################
def cut_words():
    preprocessing()
    global chinese_list
    global doc_list
    global stopwords_dict
    load_stopwords()
    fw = open('chineseNoStopWords.txt','w')
    doc_list =[]
    word_set = {}
    index = 0
    for doc in chinese_list:
        word_vector = []
        slist = doc.split(',')
        for s in slist:
            for item in jieba.cut(s):
                item = str(item.replace('\n','')) #convert to utf-8
                if item not in word_set:
                    if item not in stopwords_dict:
                        fw.write(item)
                        fw.write('\n')
                        index =  index + 1
                        word_set[item] = index
                word_vector.append(item)
        word_vector = ' '.join(word_vector)
        doc_list.append(word_vector)
    clear()
    fw.close()
##################################################################################################################################
def clear():
    global chinese_list
    global news_list
    global stopwords_dict
    news_list = []
    chinese_list = []
    stopwords_dict = {}
##################################################################################################################################
def create_dir():   
    save_dir='res_'+sys.argv[1]
    if not os.path.exists(save_dir):
        print "++++++++++++++++create dir: "+save_dir+"+++++++++++++++++++"
        os.mkdir(save_dir)
##################################################################################################################################
def main():
    """
    Downloads and analyzes a bunch of random Wikipedia articles using
    online VB for LDA.
    """
    global D
    global doc_list
    global last_gamma_file
    cut_words()
    print D
    print len(doc_list)
    # The number of documents to analyze each iteration
    batchsize = 64
    # The total number of documents in Wikipedia
    #D = 500
    # The number of topics
    K = int(sys.argv[1])

    # How many documents to look at
    if (len(sys.argv) < 3):
        documentstoanalyze = int(D/batchsize)
    else:
        documentstoanalyze = int(sys.argv[1])

    # Our vocabulary
    vocab = file('./chineseNoStopWords.txt').readlines()
    #print vocab
    W = len(vocab)

    # Initialize the algorithm with alpha=1/K, eta=1/K, tau_0=1024, kappa=0.7
    olda = onlineldavb.OnlineLDA(vocab, K, D, 1./K, 1./K, 1024., 0.7)
    # Run until we've seen D documents. (Feel free to interrupt *much*
    # sooner than this.)
    print documentstoanalyze
    perplexity_set = []
    iter_set = []
    for iteration in range(0, documentstoanalyze):
        # Download some articles
        '''
        (docset, articlenames) = \
            wikirandom.get_random_wikipedia_articles(batchsize)
        '''
        docset = doc_list[iteration*batchsize:(iteration+1)*batchsize]
        # Give them to online LDA
        (gamma, bound) = olda.update_lambda(docset)
        # Compute an estimate of held-out perplexity
        (wordids, wordcts) = onlineldavb.parse_doc_list(docset, olda._vocab)
        perwordbound = bound * len(docset) / (D * sum(map(sum, wordcts)))
        print '%d:  rho_t = %f,  held-out perplexity estimate = %f' % \
            (iteration, olda._rhot, numpy.exp(-perwordbound))
        perplexity_set.append(numpy.exp(-perwordbound))
        iter_set.append(iteration)
        # Save lambda, the parameters to the variational distributions
        # over topics, and gamma, the parameters to the variational
        # distributions over topic weights for the articles analyzed in
        # the last iteration.
        if (iteration % 100 == 0 or iteration==documentstoanalyze-1):
            numpy.savetxt('./res_'+sys.argv[1]+'/lambda-%d.dat' % iteration, olda._lambda)
            numpy.savetxt('./res_'+sys.argv[1]+'/gamma-%d.dat' % iteration, gamma)
    last_gamma_file = './res_'+sys.argv[1]+'/lambda-%d.dat'%(documentstoanalyze-1)
    save_lambda_path = 'last_lambda_'+sys.argv[1]+'.txt'
    flast = open(save_lambda_path,'w')
    flast.write(last_gamma_file)
    flast.close()

if __name__ == '__main__':
    create_dir()
    main()
    #printtopics.save_topics(last_gamma_file)
    