#!/usr/bin/env python
# encoding: utf-8
"""
gen_graphml_from_pickle.py

Created by Conover, Michael D on 2012-05-02.

This script generates an intergeographic connectivity edgelist for consumption by, for example, the great circles viz.
"""

import os, sys
import cPickle as p
import networkx as nx
import graph_tools as gt


def main(g, outfile):
    with open(outfile, 'w') as fout:
        header = ["source", "target", "tweets"]
        print >> fout, "\t".join(header)
        
        
        # HACK!  Why is Rio De Janeiro as state name?  Is it from the geobasis?
        for e in g.edges(data=True):
            if e[1] != 'Rio De Janeiro':
                print >> fout, "%s\t%s\t%s" % (e[0], e[1], e[2]['weight'])
    

if __name__ == '__main__':
    from optparse import OptionParser
    parser = OptionParser()
    
    parser.add_option("-i", "--infile", help="Location of input network pickle (dat format).", 
                    type="str", dest="infile", default="/u/midconov/anatwit/ows/network/ows-02/ows-02_retweet-g_state.pickle" )                 
    parser.add_option("-o", "--outfile", help="Location of output edgelist representation of network.", 
                    type="str", dest="outfile", default="/tmp/foo.edgelist" )
    parser.add_option("-a", "--alpha", help="Value of multiscale backbone alpha parameter.", 
                    type="float", dest="alpha", default=.01 )                                        
    options, args = parser.parse_args(sys.argv[1:])
    
    infile = options.infile
    outfile = options.outfile
    alpha = options.alpha
    
    dat = p.load(open(infile))
    g = dat['graph']
    g = gt.convert_to_multiweighted(g)
    g = gt.extract_backbone(g, alpha=alpha)
    
    main(g, outfile)
    
    print "Wrote to: %s" % outfile
    
