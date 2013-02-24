#!/usr/bin/env python
# encoding: utf-8
"""
quick_states_on_time_number_of_tweets.py

Created by Conover, Michael D on 2012-09-19.

This script ..
"""

from owsutils.tweet_factories import BasicDiskTweetFactory
import os, sys
from collections import defaultdict
import types
import re
from datetime import date
import cPickle as pickle
import time
import gc

def main(infile):
    tf = BasicDiskTweetFactory(infile)
    print 'loading', infile

    mintime = 99999999999
    maxtime = -1
    numtweets = 0
    originating_users = set()
    
    gc.disable()
    
    for t in tf.get_tweets():
        if t is not None:                                    
            try:                
                try:
                    ts = int(t.time)
                    sn = t.screen_name.lower()
                    
                    if ts < mintime:
                        mintime = ts
                    if ts > maxtime:
                        maxtime = ts
                        
                    originating_users.add(sn)
                        
                except(UnicodeDecodeError):
                    print "UnicodeDecodeError\t%s" % sn

            except(AttributeError):
                    print "AttributeError"
        else:
            print 'Malformed Tweet warning in: ', infile
    gc.enable()
    
    
    print "Min Time: %s" % (time.ctime(mintime))
    print "Max Time: %s" % (time.ctime(maxtime))
    print "Originating Users: %s" % (len(originating_users))
    
if __name__ == '__main__':
    from optparse import OptionParser
    parser = OptionParser()

    parser.add_option("-i", "--infile", help="Location of tweet file.", 
                    type="str", dest="infile", default="/l/cnets/research/mdc/data/twitter/tweets/ows/ows_tweets-02.dat.gz")                 
                    
    options, args = parser.parse_args(sys.argv[1:])
    
    infile = options.infile
    
    main(infile)
    
