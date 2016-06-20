#!/bin/sh
PYTHON_BIN_PATH="/usr/local/bin/"
date
rm -rf ./res_10/*
rm -rf ./topic_txt_10/*
rm -rf /home/xxmonitor/xxmonitor/topic_txts/ios_feedback_lda//xxapp_101/topic_10/*
cd /home/xxstatistics/userfigure/feedback/ios_xxfeedback_lda_101/
$PYTHON_BIN_PATH/python topicmain.py 10
$PYTHON_BIN_PATH/python printtopics.py 10
$PYTHON_BIN_PATH/python savemonthtopics.py


