#!/usr/bin/env python
# encoding: utf-8
"""
gen_descriptive_statistics_from_slices.py

Created by Conover, Michael D on 2012-04-30.

This script will generate temporal descriptive statistics based on 
a series of network snapshots located in a common directory.  

"""

import os, sys
import cPickle as pickle
import networkx as nx
import numpy as np
from scipy import stats

import graph_tools.graph_tools as gt
from graph_tools.graph_factories import GraphSliceFactory
from owsutils.tictoc import TicToc

def main(slicedir, outfile_base):
    sf = GraphSliceFactory(slicedir)
        
    slice_stat = {}
    stat_keys = [\
            'nodes', 'edges', 'density', \
            'mean_indegree', 'std_indegree', 'skew_indegree', 'max_indegree', \
            'mean_instrength', 'std_instrength', 'skew_instrength', 'max_instrength', \
            'mean_outdegree', 'std_outdegree', 'skew_outdegree', 'max_outdegree', \
            'mean_outstrength', 'std_outstrength', 'skew_outstrength', 'max_outstrength', \
            'mean_cc', 'std_cc', 'skew_cc', \
            'num_components', 'size_max_comp', 'density_max_comp', \
            'lcc_mean_indegree', 'lcc_mean_outdegree', 'lcc_mean_instrength', 'lcc_mean_outstrength', \
            'lcc_max_indegree', 'lcc_max_outdegree', 'lcc_max_instrength', 'lcc_max_outstrength', 'mean_compsize', 'std_compsize', 'skew_compsize']    
    for key in stat_keys:
        slice_stat[key] = [0 for i in range(sf.slicecount)]
    
    print "Writing to: %s.csv" % outfile_base
    # GGPlot2
    with open("%s.csv" % outfile_base, 'w') as fout_csv:
        # Sergey
        with open("%s.dat" % outfile_base, 'w') as fout:  
            print >> fout, "step\t" + "\t".join(stat_keys)
            print >> fout_csv, "index\tkey\tvalue"
            idx = 0
            for g in sf.get_slices(verbose=False):
                with TicToc("Index: %s  (%s Nodes, %s Edges)" % (idx, g.number_of_nodes(), g.number_of_edges()), print_close=True):
                    simple_g = gt.convert_to_multiweighted(g, directed=True)
                    undirected_g = gt.convert_multi_to_simple(g)
                    
                    if simple_g.number_of_nodes() > 0:
                
                        # Connected Component Computations
                        comps = nx.connected_components(undirected_g)
                        max_comp = []
                        for c in comps:
                            if len(c) > len(max_comp):
                                max_comp = c
                    
                        component_sizes = [len(c) for c in comps]
                    
                    
                        indeg = simple_g.in_degree().values()
                        instr = simple_g.in_degree(weighted=True).values()
                    
                        outdeg = simple_g.out_degree().values()               
                        outstr = simple_g.out_degree(weighted=True).values()
        
                        clust = nx.clustering(undirected_g).values()
                    
                
                        slice_stat['nodes'][sf.idx] = simple_g.number_of_nodes()
                        slice_stat['edges'][sf.idx] = simple_g.number_of_edges()        
                        slice_stat['density'][sf.idx] = nx.density(simple_g)
                
                        # In Degree / Strength
                        slice_stat['mean_indegree'][sf.idx] = np.mean(indeg)
                        slice_stat['std_indegree'][sf.idx] = np.std(indeg)
                        slice_stat['skew_indegree'][sf.idx] = stats.skew(indeg)
                        slice_stat['max_indegree'][sf.idx] = max(indeg)
                    
                        slice_stat['mean_instrength'][sf.idx] = np.mean(instr)
                        slice_stat['std_instrength'][sf.idx] = np.std(instr)
                        slice_stat['skew_instrength'][sf.idx] = stats.skew(instr)
                        slice_stat['max_instrength'][sf.idx] = max(instr)
                    
                    
                        # Out Degree / Strength
                        slice_stat['mean_outdegree'][sf.idx] = np.mean(outdeg)
                        slice_stat['std_outdegree'][sf.idx] = np.std(outdeg)
                        slice_stat['skew_outdegree'][sf.idx] = stats.skew(outdeg)
                        slice_stat['max_outdegree'][sf.idx] = max(outdeg)
                    
                        slice_stat['mean_outstrength'][sf.idx] = np.mean(outstr)
                        slice_stat['std_outstrength'][sf.idx] = np.std(outstr)
                        slice_stat['skew_outstrength'][sf.idx] = stats.skew(outstr)
                        slice_stat['max_outstrength'][sf.idx] = max(outstr)
                    
                    
                        slice_stat['mean_cc'][sf.idx] = np.mean(clust)
                        slice_stat['std_cc'][sf.idx] = np.std(clust)
                        slice_stat['skew_cc'][sf.idx] = stats.skew(clust)
                
                        if True:
                            # Statistics for Largest Connected Component
                            with TicToc("LCC Subgraph"):
                                max_comp_g = undirected_g.subgraph(max_comp)
                            with TicToc("LCC Degrees"):
                                indeg = simple_g.in_degree(max_comp).values()
                                instr = simple_g.in_degree(max_comp, weighted=True).values()
                    
                                outdeg = simple_g.out_degree(max_comp).values()               
                                outstr = simple_g.out_degree(max_comp, weighted=True).values()
                            with TicToc("LCC Calculations Other"):    
                                slice_stat['num_components'][sf.idx] = len(comps) 
                                slice_stat['size_max_comp'][sf.idx] = max_comp_g.number_of_nodes()
                                slice_stat['density_max_comp'][sf.idx] = nx.density(max_comp_g) 
                    
                                slice_stat['lcc_mean_indegree'][sf.idx] = np.mean(indeg)
                                slice_stat['lcc_mean_outdegree'][sf.idx] = np.mean(outdeg)
                                slice_stat['lcc_mean_instrength'][sf.idx] = np.mean(instr)
                                slice_stat['lcc_mean_outstrength'][sf.idx] = np.mean(instr)
                    
                                slice_stat['lcc_max_indegree'][sf.idx] = max(indeg) 
                                slice_stat['lcc_max_outdegree'][sf.idx] = max(outdeg) 
                                slice_stat['lcc_max_instrength'][sf.idx] = max(instr) 
                                slice_stat['lcc_max_outstrength'][sf.idx] = max(outstr) 
                
                                slice_stat['mean_compsize'][sf.idx] = np.mean(component_sizes)
                                slice_stat['std_compsize'][sf.idx] = np.std(component_sizes)
                                slice_stat['skew_compsize'][sf.idx] = stats.skew(component_sizes)
     
                        # ggplot2 Format
                        for key in stat_keys:
                            print >> fout_csv, "%s\t%s\t%s" % (idx, key, slice_stat[key][idx])
                            #print "%s\t%s\t%s" % (idx, key, slice_stat[key][idx])
                    
                        # Sergey Format
                        data_str = "\t".join([str(slice_stat[key][idx]) for key in stat_keys])
                        print >> fout, "%s\t%s" % (idx, data_str)
                    


                    
                idx += 1
        
    print "Wrote to: %s.csv" % outfile_base
    print "Wrote to: %s.dat" % outfile_base    
    
if __name__ == '__main__':
    from optparse import OptionParser
    parser = OptionParser()
    
    parser.add_option("-i", "--slicedir", help="Location of input directory containing timeslices.", 
                    type="str", dest="slicedir", default="%s/ows/network/ows-30/ows-30_retweet-r168/" % os.environ['ANADIR'] )                 
    parser.add_option("-o", "--outfile", help="Base location of output file (this is the base that will take .csv and .dat)", 
                    type="str", dest="outfile_base", default="%stwitter/foo.out" % os.environ['ANADIR'] )
    # parser.add_option("-v", "--verbose", help="Allow verbose output.", 
    #                dest="verbose", action="store_true")                                    
    options, args = parser.parse_args(sys.argv[1:])
    
    slicedir = options.slicedir
    outfile_base = options.outfile_base
    
    main(slicedir, outfile_base)
    
