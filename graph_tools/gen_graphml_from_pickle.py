#!/usr/bin/env python
# encoding: utf-8
"""
gen_graphml_from_pickle.py

Created by Conover, Michael D on 2012-05-02.

This script ..
"""

import os, sys
import cPickle as p
import networkx as nx
import graph_tools as gt


def main(g, outfile):
    nx.write_graphml(g, outfile)

if __name__ == '__main__':
    from optparse import OptionParser
    parser = OptionParser()
    
    parser.add_option("-i", "--infile", help="Location of input network pickle (dat format).", 
                    type="str", dest="infile", default="%stwitter/foo.in" % os.environ['ANADIR'] )                 
    parser.add_option("-o", "--outfile", help="Location of output graphml representation of network.", 
                    type="str", dest="outfile", default="%stwitter/foo.out" % os.environ['ANADIR'] )
    parser.add_option("-m", "--multiweighted", help="Convert multigraph to simple graph with weights determined by number of edges.", 
                    dest="multiweighted", action="store_true")       
    parser.add_option("-d", "--directed", help="Construct as directed graph.", 
                        dest="directed", action="store_true")                                                 
    options, args = parser.parse_args(sys.argv[1:])
    
    infile = options.infile
    outfile = options.outfile
    multiweighted = options.multiweighted
    directed = options.directed
    
    dat = p.load(open(infile))
    g = dat['graph']
    
    if multiweighted:
        g = gt.convert_to_multiweighted(g, directed)
        
    main(g, outfile)
    
    print "Wrote to: %s" % outfile
    
