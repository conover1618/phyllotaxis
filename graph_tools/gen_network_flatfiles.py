# Author: MDC, Apr 27

# This script creates edgelists and properties files for retweet / reply graphs 
# describing communication among users based on pipe-delimited flat files.  

# edgelist: sstatus AS eid, retweet_user AS source, screen_name AS target;
# edgeprop: status AS eid, status AS status, time AS ts;
# nodeprop: sn AS nid, sn AS sn, mode_loc AS mode_loc


# TODO:  Improve edge criterion processing via inclusion of dectorator pattern.  

import os, sys

from owsutils.tweet_factories import BasicDiskTweetFactory
from owsutils.simple_progress import ProgressMeter
from collections import defaultdict
import owsutils.utils as owsutils
from owsutils.tictoc import TicToc

# Creates an edge tuple based on the formatting requirements of retweets
def edge_factory(t, etype):
    status = t.status
    ts = t.time
    sn = t.screen_name.lower()
    reply_user = t.reply_user.lower()
    retweet_user = t.retweet_user.lower()
    locstr = t.location.lower()
    
    etup = None
    if etype=='retweet':
        etup = (status, retweet_user, sn)
    elif etype=='mention':
        etup = (status, sn, reply_user)
    else:
        sys.exit("Invalid tweet type. [%s]" % (etype))
    return etup


    
# Creates an edge property entry (status is duplicated as it's the id and a property)
def edgeprop_factory(t):
    status = t.status
    ts = t.time
    
    return (status, status, ts)
  
# Must be a mention
def edge_crtierion_mention(t, node_prop_val):
    try:
        sn = t.screen_name.lower()
        reply_user = t.reply_user.lower()

        if reply_user == '':
            return False

        return True
    except KeyError, e:
        return False
          

# Must be a retweet
def edge_crtierion_retweet(t, node_prop_val):
    try:
        sn = t.screen_name.lower()
        retweet_user = t.retweet_user.lower()

        if retweet_user == '':
            return False

        return True
    except KeyError, e:
        return False

# Locstr for the retweeted and retweeting user must be non-null
def edge_crtierion_retweet_locstr(t, node_prop_val):
    try:
        sn = t.screen_name.lower()
        retweet_user = t.retweet_user.lower()
   
        sn_locstr = node_prop_val[sn]['locstr'].strip()
        rt_locstr = node_prop_val[retweet_user]['locstr'].strip()

        if sn_locstr == '' or rt_locstr == '':
            return False

        return True
    except KeyError, e:
        return False       


# Create dictionary of node -> property mappings based on data contained in tweet files
# Note, not every node will have an entry in the property file.  Imagine the case where 
# someone is retweeted, but we do not observe any content originating from them as a singleton. 
# In this case, we will not know their location, for example.

# def get_node_props(tweetfile):
#     print "Processing Node Properties"
#     tf = BasicDiskTweetFactory(tweetfile)
#     pm = ProgressMeter(999999999)
#     
#     node_prop_val = {}
#     for t in tf.get_tweets():
#         if t is not None:
#             try:
#                 try:      
#                     sn = t.screen_name.lower()
#                     locstr = t.location.lower()
#                         
#                     if sn not in node_prop_val:
#                         node_prop_val[sn] = {}
#                         node_prop_val[sn]['locstr'] = []
#                     
#                     node_prop_val[sn]['locstr'].append(locstr)
#                     pm.update()
#                 except(UnicodeDecodeError):
#                     print "UnicodeDecodeError\t%s" % sn
#             except(AttributeError):
#                  print "AttributeError"
#         else:
#             pass
#     
#     Final pre-processing of node_prop_val
#     for (node, prop_val) in node_prop_val.items():
#         # Compute most common location string for each user
#         locstr_count = defaultdict(int)
#     
#         for locstr in node_prop_val[node]['locstr']:
#             locstr_count[locstr] += 1
#     
#         max_count = -1
#         mode_locstr = ''
#         for (locstr, count) in locstr_count.items():
#             if count > max_count:
#                 mode_locstr = locstr
#                 max_count = count
#         node_prop_val[node]['modeloc'] = mode_locstr
#         
#     return node_prop_val
    
# Alternate version, here we simply take the first location we see.
def get_node_props(tweetfile):
    print "Processing Node Properties"
    tf = BasicDiskTweetFactory(tweetfile)
    pm = ProgressMeter(999999999)
    
    node_prop_val = {}
    for t in tf.get_tweets():
        if t is not None:
            try:
                try:      
                    sn = t.screen_name.lower()
                    locstr = t.location.lower()
                        
                    if sn not in node_prop_val:
                        node_prop_val[sn] = {}
                        node_prop_val[sn]['locstr'] = locstr
                    pm.update()
                except(UnicodeDecodeError):
                    print "UnicodeDecodeError\t%s" % sn
            except(AttributeError):
                 print "AttributeError"
        else:
            pass
        
    return node_prop_val


def main(tweetfile, edge_type, outdir, key, nullstr):
    
    node_prop_val = get_node_props(tweetfile)
    print "Found %s Nodes with Properties" % len(node_prop_val) 
    tf = BasicDiskTweetFactory(tweetfile)
    
    # These are generic methods used to accomodate different formatting for retweets and replies
    edge_criterion = False
    if edge_type == 'retweet':
        edge_criterion = edge_crtierion_retweet
    if edge_type == 'mention':
        edge_criterion = edge_crtierion_mention
    
    eid_proptup = {}
    eid_edgetup = {}
    
    incl_nodes = set()
    
    rt_count = defaultdict(int)
    edge_count = 0
    dupe_count = 0
    
    print "Reading Edges"
    pm = ProgressMeter(999999999)
    for t in tf.get_tweets():
        if t is not None:
            try:
                try:   
                    eid = t.status

                    if edge_criterion(t, node_prop_val):
                        if eid in eid_edgetup:
                            dupe_count += 1
                            
                        
                        eid_proptup[eid] = edgeprop_factory(t)
                        eid_edgetup[eid] = edge_factory(t, edge_type)
                        
                        # Add the source and target to the set of nodes included in the graph
                        # This allows us to only output node properties for relevant nodes
                        incl_nodes.add(eid_edgetup[eid][1])
                        incl_nodes.add(eid_edgetup[eid][2])
                        
                        rt_count[eid_edgetup[eid][1]] += 1
                        edge_count += 1
                    pm.update()
                except(UnicodeDecodeError):
                    print "UnicodeDecodeError\t%s" % sn

            except(AttributeError):
                 print "AttributeError"

        else:
            pass
    
    # print sum(rt_count.values())
    # print "Edge Count: %s" % edge_count
    # print "Dupe Count: %s" % dupe_count
    
    edge_prop_file = "%s%s.edgeprop" % (outdir, key)
    edge_list_file = "%s%s.edgelist" % (outdir, key)
    node_prop_file = "%s%s.nodeprop" % (outdir, key)
    
    with open(edge_prop_file, 'w') as fout:
        header = ['eid', 'status', 'ts']
        print >> fout, "\t".join(header)
        
        for (eid, proptup) in eid_proptup.items():
            print >> fout, "\t".join([str(i) for i in proptup])
  
    with open(edge_list_file, 'w') as fout:
        header = ['eid', 'source', 'target']
        print >> fout, "\t".join(header)
        
        for (eid, edgetup) in eid_edgetup.items():
            print >> fout, "\t".join([str(i) for i in edgetup])
    
    with open(node_prop_file, 'w') as fout:
        header = ['nid', 'sn', 'locstr']
        print >> fout, "\t".join(header)
        
        # Print output for all nodes, even those missing properties.  
        # Fill in with nullstr in the absence of property data.
        for nid in incl_nodes:
            locstr = nullstr
            if nid in node_prop_val:
                prop_val = node_prop_val[nid]
                locstr = node_prop_val[nid]['locstr']
                    
                # Ignore Mode Location Strings with Length less than One
                if locstr.strip() == '' or len(locstr) <= 1:
                    locstr = nullstr
                
            print >> fout, "%s\t%s\t%s" % (nid, nid, locstr)
    
    print "%s Nodes (%s with properties)" % (len(incl_nodes), len(set(node_prop_val.keys()).intersection(incl_nodes)))
    print "%s Edges" % len(eid_edgetup)
    
    print ""
    print "Wrote to: %s" % edge_prop_file
    print "Wrote to: %s" % edge_list_file
    print "Wrote to: %s" % node_prop_file
        
        

if __name__ == '__main__':
    from optparse import OptionParser
    parser = OptionParser()
    
    parser.add_option("-i", "--tweetfile", help="Location of pipe-delimited tweet file to process.", 
                    type="str", dest="tweetfile", default="%stwitter/tweets/ows/ows_tweets_small.dat.gz" % os.environ['DATADIR'] )                 
    parser.add_option("-e", "--edgetype", help="Type of edge to process. (retweet|reply)", 
                    type="str", dest="edgetype", default="retweet" )
    parser.add_option("-o", "--archivebase", help="Directory in which to store resulting graph archive directory. This is the *BASE* network directory.", 
                    type="str", dest="archivebase", default="%stwitter/ows/network" % os.environ['ANADIR'] )    
    parser.add_option("-k", "--key", help="Key to identify output.", 
                    type="str", dest="key", default="ows"  )
    parser.add_option("-n", "--nullstr", help="String to use for null properties.", 
                    type="str", dest="nullstr", default="$#"  )
                    
    options, args = parser.parse_args(sys.argv[1:])
    
    tweetfile = options.tweetfile
    edgetype = options.edgetype
    key = options.key    
    outdir = "%s%s/" % (options.archivebase, key)
    nullstr = options.nullstr
    
    owsutils._mkdir(outdir)
    
    key = "%s_%s" % (key, edgetype)
    main(tweetfile, edgetype, outdir, key, nullstr)
    
    



