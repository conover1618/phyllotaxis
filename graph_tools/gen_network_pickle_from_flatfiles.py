# Author: MDC, Apr 25

# This script produces a single pickle containing the networkx graph and metadata 
# specified in the target edgelist and property files.  
# It specifies arguments that allow for transforming the graph in terms of 
# directedness, weights, etc.  

import os, sys
import networkx as nx
import cPickle as p
import graph_tools as gt
from graph_factories import GraphFromFlatFilesFactory
from phyllotaxis.mdcutils.tictoc import TicToc

def stats(edgelist, nid_prop_val):
    el_statuses = set()
    el_nodes = set()
    el_edges = set()
    el_und_edges = set()
            
    el_total_entries = 0
    el_recip_edges = 0
    el_multi_edges = 0
  
    for e in edgelist:
        eid = e[0]
        source = e[1]
        target = e[2]
        
        el_statuses.add(eid)
        el_nodes.add(source)
        el_nodes.add(target)
        
        if (source, target) in el_edges:
            el_multi_edges += 1
            
        if (target, source) in el_edges:
            el_recip_edges += 1
        
        el_edges.add((source, target))
        
        el_und_edges.add((source, target))
        el_und_edges.add((target, source))        
        
        el_total_entries += 1
        
    print "%s Edgelist Nodes" % len (el_nodes)
    print "%s Statuses" % len(el_statuses)
    print "%s Directed Edges" % len(el_edges)
    print "%s Undirected Edges" % (len(el_und_edges) / 2.0)
    print "%s Edge Entries" % el_total_entries
    print "%s Recip Edges" % el_recip_edges
    print "%s Multi Edges" % el_multi_edges
    
    print ""
    
    print "%s NID Nodes"
    print "%s Nodes in Edgelist w/o Props" % (len(el_nodes.difference(nid_prop_val.keys())))
    
    


if __name__ == "__main__":
    from optparse import OptionParser
    parser = OptionParser()
    
    parser.add_option("-i", "--indir", help="Location of input flatfiles.", 
                    type="str", dest="indir", default="%s/twitter/ows/network/" % os.environ['ANADIR'] )                 
    parser.add_option("-o", "--outdir", help="Location to write graph pickle.", 
                    type="str", dest="outdir", default="%s/twitter/ows/network/" % os.environ['ANADIR'] )
    parser.add_option("-k", "--key", help="Key identifier for graph flatfiles + output.", 
                    type="str", dest="key", default="ows_retweet" )   
    parser.add_option("-d", "--directed", help="Construct as directed graph.", 
                        dest="directed", action="store_true")             
    parser.add_option("-m", "--multiweighted", help="Construct as weighted graph using the number of edges between two nodes as a weighting factor.", 
                        dest="multiweighted", action="store_true")
                                  
    options, args = parser.parse_args(sys.argv[1:])
    
    indir = options.indir
    outdir = options.outdir
    key = options.key
    directed = options.directed
    multiweighted = options.multiweighted
    
    print "Key: %s" % key
    gf = GraphFromFlatFilesFactory(indir, key, directed, multiweighted)
    g = gf.get_graph()
    
    outfile = "%s%s.pickle" % (outdir, key) 
    
    # Annotate and output
    dat = {}
    dat['graph'] = g
    dat['meta'] = {}
    dat['meta']['edgelist_file'] = gf.edgelistfile
    dat['meta']['nodeprop_file'] = gf.nodepropfile
    dat['meta']['edgeprop_file'] = gf.edgepropfile
    dat['meta']['directed'] = gf.directed
    dat['meta']['multiweighted'] = gf.multiweighted
    
    with TicToc("Writing to Pickle"):
        p.dump(dat, open(outfile,'w'))
    
    print "%s Nodes in Graph" % g.number_of_nodes()
    print "%s Edges in Graph" % g.number_of_edges()

    print ""
    print "Wrote to: %s" % outfile