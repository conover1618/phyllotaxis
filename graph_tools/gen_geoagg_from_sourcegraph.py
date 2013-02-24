#!/usr/bin/env python
# encoding: utf-8
"""
gen_geoagg_from_sourcegraph.py

Created by Conover, Michael D on 2012-04-30.

This script consumes a user-user graph pickle and outputs a graph 
in which nodes are locations at the specified geographic resolution.  
Multiple edges between locations are preserved with their original 
properties, and this output is suitable input to the script which
generates individual timeslices from a network pickle.

"""

import os, sys
import owsutils.utils as owsutils
import cPickle as p
import networkx as nx

def main(picklefile, geores, outdir, key, nullstr):
    print "Loading: %s" % picklefile
    dat = p.load(open(picklefile))
    g = dat['graph']
    
    locs = set()
    
    for tup in g.nodes(data=True):
        try:
            locval = tup[1][geores]
            if locval != nullstr:
                locs.add(tup[1][geores])
                
        except AttributeError, e:
            print "Error Reading Resolution: %s" % tup
    
    print "Generating Geographic Aggregate Graph"
    geo_g = nx.MultiDiGraph()
    
    # Add edges to a new graph where nodes are geolocation entries
    # preserving edge attributes.  Do not add edges where one of the 
    # adjacent nodes does not have satisfactory geolocation data.
    for e in g.edges(data=True):
        source = e[0]
        target = e[1]
        attrs = e[2]
        
        source_geoloc = g.node[source][geores]
        target_geoloc = g.node[target][geores]
        
        if source_geoloc != nullstr and target_geoloc != nullstr:
            geo_g.add_edge(source_geoloc, target_geoloc, attr_dict=attrs)

    geo_dat = {}
    geo_dat['meta'] = dat['meta']
    geo_dat['meta']['geores'] = geores
    geo_dat['graph'] = geo_g
    
    outfile = "%s%s-g_%s.pickle" % (outdir, key, geores)
    print "Geo-Aggregate Network"
    print "%s Nodes" % (geo_g.number_of_nodes())
    print "%s Edges" % (geo_g.number_of_edges())

    p.dump(geo_dat, open(outfile, 'w'))
    print "Wrote to: %s" % outfile
        

if __name__ == '__main__':
    from optparse import OptionParser
    parser = OptionParser()

    parser.add_option("-p", "--picklefile", help="Loation of graph pickle.", 
                   type="str", dest="picklefile", default="%stwitter/ows/network/ows_small_retweet.pickle" % os.environ['ANADIR'] )                 
    parser.add_option("-o", "--outdir", help="Root location to write timesliced graph pickles.", 
                   type="str", dest="outdir", default="%stwitter/ows/network" % os.environ['ANADIR'] ) 
    parser.add_option("-n", "--nullstr", help="This value specifies a null string in the geoloc field.", 
                    type="str", dest="nullstr", default="#%" )
    parser.add_option("-g", "--geores", help="Level of geospatial aggregation. (city | state | country)", 
                  type="str", dest="geores", default="state" )
                  

    options, args = parser.parse_args(sys.argv[1:])

    picklefile = options.picklefile
    outdir = options.outdir
    geores = options.geores
    nullstr = options.nullstr
    
    key = "%s" % (picklefile[picklefile.rfind('/')+1:picklefile.rfind('.')])
    
        
    owsutils._mkdir(outdir)

    main(picklefile, geores = geores, outdir = outdir, key=key, nullstr=nullstr)