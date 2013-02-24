#!/usr/bin/env python
# encoding: utf-8
"""
gen_intergeo_strength_matrix.py

Created by Conover, Michael D on 2012-05-02.

This script consumes a geoaggregate networkx pickle (dat w/ meta) and produces a file
describing the strength of connections between all pairs geolocations.  Additionally,
we report normalizations of these weights in terms of in-strength and out-strength. 

Called as: python gen_intergeo_strength_matrix.py -i /u/midconov/anatwit/ows/network/ows/ows_retweet-g_state.pickle -o /u/midconov/anatwit/ows/network/ows/intergeo/ 

"""

import os, sys
import cPickle as p
import networkx as nx
import graph_tools.graph_tools as gt
from collections import defaultdict
from owsutils.tictoc import TicToc
import owsutils.utils as owsutils

# Consumes a graph and, optionally, a list of locations to forcibly include
# and returns a dict mapping location -> location -> weight 

def get_intergeo_weight(g, geobasis=[]):
    # Tracks the proportion of traffic from source to target, non-normalized
    source_target_weight = {}
    all_locs = set([node[0] for node in g.nodes(data=True)])
    
    
    if geobasis != []:
        for loc in geobasis:
            source_target_weight[loc] = defaultdict(int)
    else:
        for loc in all_locs:
            source_target_weight[loc] = defaultdict(int)


    for e in g.edges(data=True):
        source = e[0]
        target = e[1]
        attr = e[2]
        weight = attr['weight']
        if source in geobasis and target in geobasis:
            source_target_weight[source][target] = weight
    return source_target_weight

           

# Takes a graph, a key, a geobasis list defining optionally the list of locations that must be evaluated, and an output directory
def main(g, key, outdir, geobasis=[]):
    g = gt.convert_to_multiweighted(g, directed=True)
    source_target_weight = get_intergeo_weight(g, geobasis)
        
    # Get in / out strengths for all nodes
    loc_outstrength = defaultdict(int)
    loc_instrength = defaultdict(int)
    for e in g.edges(data=True):
        loc_outstrength[e[0]] += e[2]['weight']
        loc_instrength[e[1]] += e[2]['weight']
    
    incl_locs = geobasis
    if geobasis == []:
        outlocs = set(loc_outstrength.keys())
        inlocs = set(loc_instrength.keys())
        incl_locs = list(outlocs.union(inlocs))

    
    intergeo_file = "%s%s-intergeo.csv" % (outdir, key)
    with open(intergeo_file, 'w') as fout:
        header = ['source', 'target', 'weight', 'sourcenorm', 'targetnorm']
        print >> fout, "\t".join(header)  
        
        for source_loc in incl_locs:
            for target_loc in incl_locs:
                weight = source_target_weight[source_loc][target_loc]
                
                sourcenorm = 0
                targetnorm = 0
                
                try:
                    sourcenorm = weight / float(loc_outstrength[source_loc])
                    targetnorm = weight / float(loc_instrength[target_loc])
                    #print "Success: %s / %s = %s" % (weight, loc_outstrength[source_loc], sourcenorm)
                except(ZeroDivisionError):
                    pass
                    #print "ZeroDivisionError: %s %s" % (source_loc, target_loc)
                    
                # Here we report the source, target, weight, and two ways of normalizing the weight
                print >> fout, "%s\t%s\t%s\t%s\t%s" % (source_loc, target_loc, weight, sourcenorm, targetnorm)


    ratio_file = "%s%s-intergeo-ratio.csv" % (outdir, key)
    with open(ratio_file, 'w') as fout:
        header = ['loc', 'outstrength', 'instrength', 'ratio']
        print >> fout, "\t".join(header)
        for loc in incl_locs:
            instr = loc_instrength[loc]
            outstr = loc_outstrength[loc]
            ratio = 0.0
            
            try:
                ratio = outstr / float(instr)
            except:
                pass
            print >> fout, "%s\t%s\t%s\t%s" % (loc, loc_outstrength[loc], loc_instrength[loc], ratio)

    # Here we print a cumulative distribution ranking states by most contributions
    outcdf_file = "%s%s-intergeo-out-cdf.csv" % (outdir, key)
    with open(outcdf_file, 'w') as fout:
        header = ['rank', 'loc', 'outstrength', 'cdf']
        print >> fout, "\t".join(header)
        
        sorted_loc_outstrength = owsutils.sortdictbyval(loc_outstrength, n=len(loc_outstrength))
        rank = 0
        cdf = 0.0
        total_outstr = float(sum(tup[1] for tup in sorted_loc_outstrength))
        
        for (loc, outstr) in sorted_loc_outstrength:
            if loc in incl_locs:
                cdf += outstr / total_outstr
                print >> fout, "%s\t%s\t%s\t%s" % (rank, loc, outstr, cdf)
                rank += 1

    print "Wrote to: %s" % intergeo_file
    print "Wrote to: %s" % ratio_file
    print "Wrote to: %s" % outcdf_file

if __name__ == '__main__':
    from optparse import OptionParser
    parser = OptionParser()
    
    parser.add_option("-i", "--picklefile", help="Location of input pickle containing geoaggregate network dat (optionally a directory containing slices).", 
                    type="str", dest="picklefile", default="%stwitter/foo.in" % os.environ['ANADIR'] )                 
    parser.add_option("-o", "--outdir", help="Directory location of output files..", 
                    type="str", dest="outdir", default="%stwitter/foo.out" % os.environ['ANADIR'] )
    parser.add_option("-g", "--geobasis", help="File specifying set of locations to include in geobasis.", 
                    type="str", dest="geobasis", default="/u/midconov/anatwit/50states.txt" )                                
    options, args = parser.parse_args(sys.argv[1:])
    
    picklefile = options.picklefile
    outdir = options.outdir
    geobasis = options.geobasis

    # Determine whether this is a slice directory or a pickle file
    is_slices = False
    if picklefile[-1] == '/':
        is_slices = True
        
    owsutils._mkdir(outdir)
    
    if geobasis == '':
        geobasis = []
    else:
        geobasis = [line.strip() for line in open(geobasis).readlines()]
    
    if is_slices:
        for filename in os.listdir(picklefile):
            if filename.find('.pickle') > -1:
                filepath = "%s%s" % (picklefile, filename)
                with TicToc("Reading: %s" % filepath):
                    dat = p.load(open(filepath))
                g = dat['graph']
                key = "%s" % (filepath[filepath.rfind('/')+1:filepath.rfind('.')])
                with TicToc("Parsing Intergeo Network", print_close=True):
                    main(g, key, outdir, geobasis)
            
    else:
        print "Reading pickle."
        dat = p.load(open(picklefile))
        g = dat['graph']
        key = "%s" % (picklefile[picklefile.rfind('/')+1:picklefile.rfind('.')])

        main(g, key, outdir, geobasis)
    
