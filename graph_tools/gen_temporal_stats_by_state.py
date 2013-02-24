#!/usr/bin/env python
# encoding: utf-8
"""
gen_temporal_stats_by_state.py

Created by Conover, Michael D on 2012-05-31.

This script generates data describing activity levels in various states across time.
"""

import os, sys
from graph_tools.graph_factories import GraphSliceFactory
from collections import defaultdict
import owsutils.utils as owsutils

def main(slicedir, geobasis, nullstr, outfile):
    gf = GraphSliceFactory(slicedir)
    
    idx_loc_stat_val = {}
    idx = 0
    
    statkeys = ['users', 'tweets']
    for g in gf.get_slices():
        loc_stat_val = {}
        
        for loc in geobasis:
            loc_stat_val[loc] = defaultdict(int)
        
        for n in g.nodes(data=True):
            nid = n[0]
            attr = n[1]
            
            loc = attr['state']
            if loc in geobasis:
                loc_stat_val[loc]['users'] += 1
        
        for e in g.edges(data=True):
            source = e[0]
            node = g.node[source]
            loc = node['state']
            if loc in geobasis:
                loc_stat_val[loc]['tweets'] += 1
        
        idx_loc_stat_val[idx] = loc_stat_val
        idx += 1
    
    
    with open(outfile, 'w') as fout:
        header = "\t".join(['idx', 'loc', 'stat', 'val'])
        print >> fout, "%s" % header
        for (idx, loc_stat_val) in idx_loc_stat_val.items():
            for (loc, stat_val) in loc_stat_val.items():
                for stat in statkeys:
                    val = idx_loc_stat_val[idx][loc][stat]
                    print  >> fout, "%s\t%s\t%s\t%s" % (idx, loc, stat, val)
    
    print "Wrote to: %s" % outfile           

if __name__ == '__main__':
    from optparse import OptionParser
    parser = OptionParser()
    
    parser.add_option("-i", "--slicedir", help="Location of slice directory containing slice pickles.", 
                    type="str", dest="slicedir", default="/u/midconov/anatwit/ows/network/ows-02/ows-02_retweet-r168/" ) 
    parser.add_option("-g", "--geobasis", help="File specifying set of locations to include in geobasis.", 
                    type="str", dest="geobasis", default="" )
    parser.add_option("-n", "--nullstr", help="This value specifies a null string in the geoloc field.", 
                    type="str", dest="nullstr", default="#%" )
    # parser.add_option("-v", "--verbose", help="Allow verbose output.", 
    #                dest="verbose", action="store_true")                                    
    options, args = parser.parse_args(sys.argv[1:])
    
    slicedir = options.slicedir
    nullstr = options.nullstr
    geobasis = options.geobasis
    
    key = slicedir[slicedir[:-2].rfind('/') + 1:-1]
    print key
    outdir = "%sstats/" % slicedir
    owsutils._mkdir(outdir)
    outfile = "%s%s_state_stats.csv" % (outdir, key)
    
    if geobasis == '':
        geobasis = []
    else:
        geobasis = set([line.strip() for line in open(geobasis).readlines()])
        
        
    main(slicedir, geobasis, nullstr, outfile)
    
