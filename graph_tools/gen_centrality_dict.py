#!/usr/bin/env python
# encoding: utf-8
"""
new_script_template.py

Created by AUTHORNAME on DATE.

This script calculates the betweenness centrality of nodes in a networkx graph
and commits them to a pickle file.

"""

import os, sys
import networkx as nx
import cPickle as pickle


def main(infile, outfile):
    dat = pickle.load(open(infile))
    g = dat['graph']
    
    node_centrality = nx.betweenness_centrality(g)

    pickle.dump(node_centrality, open(outfile, 'w'))

if __name__ == '__main__':
    from optparse import OptionParser
    parser = OptionParser()
    
    parser.add_option("-i", "--infile", help="Location of input file.", 
                    type="str", dest="infile", default="/u/foo/twitter/foo.in")                 
    parser.add_option("-o", "--outfile", help="Location of output file.", 
                    type="str", dest="outfile", default="/u/foo/twitter/foo.out" )
    # parser.add_option("-v", "--verbose", help="Allow verbose output.", 
    #                dest="verbose", action="store_true")                                    
    options, args = parser.parse_args(sys.argv[1:])
    
    infile = options.infile
    outfile = options.outfile
    
    main(infile, outfile)
    
