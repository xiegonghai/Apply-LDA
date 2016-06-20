#!/bin/sh
date
PYTHON_BIN_PATH="/usr/local/bin/" 
rm -rf ./res_10/*
rm -rf ./topic_txt_10/*
rm -rf /home/xxmonitor/xxmonitor/topic_txts/news_lda/topic_10/*
cd /home/xxmonitor/topic_model/news_lda
$PYTHON_BIN_PATH/python topicmain.py 10
$PYTHON_BIN_PATH/python printtopics.py 10
cd /home/xxmonitor/topic_model
$PYTHON_BIN_PATH/python savemonthtopics.py

