#!/usr/bin/env python
# encoding: utf-8
"""
gen_user_hashtag_timestamp_from_tweetcorpus.py

Created by Conover, Michael D on 2012-10-31.

This script ..
"""

import os, sys
from owsutils.simple_progress import ProgressMeter
import owsutils.utils as owsutils
from owsutils.tweet_factories import BasicDiskTweetFactory

def main(tweetfile, outdir, key, targettag=""):

                        
    outfile = "%s%s_user_hashtag_timestamp.csv" % (outdir, key)
    
    max_ts = -1
    min_ts = 99999999999
    totaltweets = 0
    
    with open(outfile, 'w') as fout:
        tstups = []
        pm = ProgressMeter(999999999)
        tf = BasicDiskTweetFactory(tweetfile)
        for t in tf.get_tweets():
            if t is not None:
                try:
                    user = t.screen_name.lower()
                    tags = owsutils.getHashtags(t.text.lower())
                    ts = t.time
                    
                    for tag in tags:
                        if targettag == "" or tag == targettag: 
                            print >> fout, "%s\t%s\t%s" % (user, tag, t.time)
                    
                    if ts < min_ts:
                        min_ts = ts
                    if ts > max_ts:
                        max_ts = ts
                    totaltweets += 1
                except(AttributeError):
                     print "AttributeError"

            else:
                pass
            pm.update()

    print "Total Tweets: %s" % totaltweets
    print "Min TS: %s" % min_ts
    print "Max TS: %s" % max_ts
    print "Wrote to: %s" % outfile


    

        
        
        

if __name__ == '__main__':
    from optparse import OptionParser
    parser = OptionParser()

    parser.add_option("-i", "--tweetfile", help="Location of input tweet file.", 
                    type="str", dest="tweetfile", default="/l/cnets/research/mdc/data/twitter/tweets/ows/ows_random5k.dat.gz" )                 
    parser.add_option("-o", "--outdir", help="Location of directory into which to write output.", 
                    type="str", dest="outdir", default="/u/midconov/anatwit/ows/behavior/tags/" )
    parser.add_option("-k", "--key", help="Key identifying source corpus.", 
                    type="str", dest="key", )                  
    parser.add_option("-t", "--targettag", help="Hashtag to extract.", 
                    type="str", dest="targettag", default="" )
    options, args = parser.parse_args(sys.argv[1:])

    tweetfile = options.tweetfile
    outdir = options.outdir
    key = options.key
    targettag = options.targettag
    

    main(tweetfile, outdir, key, targettag)