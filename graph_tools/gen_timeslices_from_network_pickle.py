# Author: MDC, April 27
#
# This script will produce a series of timeslice snapshots of a networkx graph pickle.
# Each snapshot will cover a non-overlaping timerange, determined by the resolution 
# parameter.  Construction occurs by way of identifying sets of edges that fall within
# each time range and producing graphs using those edge bunches.

import os, sys
import networkx as nx
import cPickle as p
import math
import owsutils.utils as owsutils
import time
from owsutils.tictoc import TicToc

def main(picklefile, resolution, slicedir):
    with TicToc("Reading pickle from: %s" % picklefile):
        dat = p.load(open(picklefile))
    g = dat['graph']
    print "Read Graph with %s Nodes & %s Edges" % (g.number_of_nodes(), g.number_of_edges())
    
    min_ts = 99999999999
    max_ts = -1
    
    # Compute time range min and max
    for nid_a, nbrs in g.adjacency_iter():
        for nid_b, edict in nbrs.items():
            for e in edict.items():
                ts = int(e[1]['ts'])
                if ts < min_ts:
                    min_ts = ts
                if ts > max_ts:
                    max_ts = ts
    
    print "Max: %s" % max_ts
    print "Min: %s" % min_ts
    
    numbins = int(math.ceil((max_ts + .000001 - min_ts) / resolution))
    edge_slices = [[] for i in range(numbins)]
    

    print "Assigning Edges to Slicebins"
    # Iterate over every edge in the graph and assign the edge to 
    # an appropriate edge_slice according to its timestamp
    for nid_a, nbrs in g.adjacency_iter():
        for nid_b, edict in nbrs.items():
            for e in edict.items():

                ts = int(e[1]['ts'])
                
                edge_tup = (nid_a, nid_b, e[1])
                if ts >= min_ts and ts <= max_ts:
                    binidx = int((ts - min_ts) / resolution)
                    edge_slices[binidx].append(edge_tup)
    
        
    # List to track each graph in slice order
    slice_graphs = [g.subgraph([]) for i in range(numbins)]
    # Track keys for each slice
    
    slice_keys = ['' for i in range(numbins)]
    
    slice_edge_count = 0
    # Create graph according to each slice's edge bundle
    for idx in range(len(edge_slices)):
        
        slice_graph = slice_graphs[idx]
        edge_slice = edge_slices[idx]
        
        slice_graph.add_edges_from(edge_slice)
        
        sub_nodes = set()
        for (nid, prop_val) in slice_graph.nodes(data=True):
            sub_nodes.add(nid)
        
        # Copy node properties
        for nid in sub_nodes:
            slice_graph.node[nid] = g.node[nid]
            
        slice_dat = {}
        slice_dat['graph'] = slice_graph
        slice_dat['super_meta'] = dat['meta']
        slice_dat['meta'] = {}
        slice_dat['meta']['resolution'] = resolution
        slice_dat['meta']['idx'] = idx
        slice_dat['meta']['global_min_tx'] = min_ts
        slice_dat['meta']['global_max_ts'] = max_ts
        
        slicefile = "%s%s-r%s-%s.pickle" % (slicedir, key, resolution / 3600, idx)

        with TicToc("%s : %s Edges & %s Nodes\tWriting to: %s" % (idx, slice_graph.number_of_edges(), slice_graph.number_of_nodes(), slicefile)   ):     
            p.dump(slice_dat, open(slicefile, 'w'))
            
        slice_edge_count += slice_graph.number_of_edges()
    
    if slice_edge_count == g.number_of_edges():
        print "Graph & Slices are Coherent in Edge Count"
                    
if __name__ == '__main__':

    
    from optparse import OptionParser
    parser = OptionParser()
    
    parser.add_option("-p", "--picklefile", help="Loation of graph pickle.", 
                    type="str", dest="picklefile", default="%stwitter/ows/network/ows_small_retweet.pickle" % os.environ['ANADIR'] )                 
    parser.add_option("-o", "--outdir", help="Root location to write timesliced graph pickles (parent of directory).", 
                    type="str", dest="outdir", default="%stwitter/ows/network" % os.environ['ANADIR'] )  
    parser.add_option("-r", "--resolution", help="Slice resolution in hours.", 
                    type="int", dest="resolution", default=168 )    
    
    options, args = parser.parse_args(sys.argv[1:])
    
    picklefile = options.picklefile
    outdir = options.outdir
    
    key = picklefile[picklefile.rfind('/')+1:picklefile.rfind('.')]
    resolution = options.resolution * 3600  # seconds in hour

    slicedir = "%s%s-r%s/" % (outdir, key, resolution / 3600)
    owsutils._mkdir(slicedir)

    main(picklefile, resolution = resolution, slicedir = slicedir)