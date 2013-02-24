#!/usr/bin/env python
# encoding: utf-8
"""
Created by Conover, Michael D on 2012-05-01.
"""

import sys
import os
import unittest
import cPickle as pickle
import time
import networkx as nx
import graph_tools as gt
from mdcutils.tictoc import TicToc
import mdcutils.utils as owsutils

# Consume the flat file containing properties for nodes and edges
# Infer property names from column headers
def read_properties_file(filepath, delim="\t"):
    id_prop_val = {}

    with open(filepath) as fin:
        first_line = True
        idx_propname = {}
        for line in fin:
            line = line.strip().split(delim)
            if not first_line:
                id = line[0]
                if id not in id_prop_val:
                    id_prop_val[id] = {}

                for i in range(1, len(line)):
                    try:
                        propstr = idx_propname[i]
                        propval = line[i]
                    except KeyError:
                        print line

                    id_prop_val[id][propstr] = propval

            if first_line:
                for i in range(1, len(line)):
                    idx_propname[i] = line[i]

            first_line = False

    return id_prop_val
    
    
class GraphSliceFactory(object):
    '''
    This reads an ordered series of graph / metadata pickles from disk.  
    Input: The directory location of a set of timeslice graphs.  (Graph keys must be the same as name of containing directory, with slice index appended)
        ie. ows/network/ows_small_retweet-r168/ows_small_retweet-r168-12.pickle   --  where 12 is the slice index
        
    Returns just the graph object by default, but can return metadata as well.
     '''

    def __init__(self, slicedir):
        if slicedir[-1] == '/':
            slicedir = slicedir[:len(slicedir) - 1]
        self.slicedir = slicedir
        
        self.key = os.path.split(slicedir)[1]
        self.slicecount = len(os.listdir(slicedir))
        self.idx = 0

        

    def get_slices(self, verbose=False, metadata = False):  
        
        numslices = 0
        for filename in os.listdir(self.slicedir):
            if filename.find('.pickle') > -1:
                numslices += 1
                
        idxs = [i for i in range(0, numslices)]
        
        for idx in idxs:
            self.idx = idx
            filepath = "%s/%s-%s.pickle" % (self.slicedir, self.key, idx)
            
            if verbose:
                print "Reading: %s" % filepath
                
            dat = pickle.load(open(filepath))
            try:
                if metadata:
                    yield dat
                else:
                     yield dat['graph']
            except(ValueError, IndexError):
                yield None


class GraphFromFlatFilesFactory(object):
    '''
    This returns a graph object given a set of node prop, edge prop, and edgelist files.
     '''
     
    def __init__(self, inputdir, key, directed, multiweighted):
        self.inputdir = inputdir
        self.key = key
        self.directed = directed
        self.multiweighted = multiweighted
        self.edgelistfile = "%s%s.edgelist" % (self.inputdir, self.key) 
        self.edgepropfile = "%s%s.edgeprop" % (self.inputdir, self.key) 
        self.nodepropfile = "%s%s.nodeprop" % (self.inputdir, self.key)
        
    def get_graph(self):
        
        with TicToc("Compiling Graph"):
            g = None
            if self.directed:
                g = nx.MultiDiGraph()
            else:
                g = nx.MultiGraph()

            with TicToc("Reading Edge List"):
                edgelist = self.read_edgelist(self.edgelistfile)

            with TicToc("Reading Edge Properties"):
                eid_prop_val = read_properties_file(self.edgepropfile)

            with TicToc("Reading Node Properties"):
                nid_prop_val = read_properties_file(self.nodepropfile)

            with TicToc("Creating Edge Bunch"):
                ebunch = self.create_ebunch_from_idpropval_edgelist(eid_prop_val, edgelist)

            with TicToc("Creating Node Bunch"):
                nbunch = self.create_nbunch_from_idpropval(nid_prop_val)

            with TicToc("Adding Nodes"):
                g.add_nodes_from(nbunch)

            with TicToc("Adding Edges"):
                g.add_edges_from(ebunch)

            if self.multiweighted:
                g = gt.convert_to_multiweighted(g, self.directed)
        

        return g
        
        
        
    def read_edgelist(self, filepath):
        edgelist = owsutils.count_lines_in_file_get_array(filepath)
        
        with open(filepath) as fin:
            first_line = True
            idx = 0
            for line in fin:
                line = line.strip().split("\t")

                if not first_line:
                    print line
                    eid = line[0]
                    source = line[1]
                    target = line[2]

                    edgelist[idx] = (eid, source, target)
                    idx += 1

                first_line = False  
        print "Edgelist Length: %s" % len(edgelist)
        print "IDX: %s" % idx  
        print "%s" % edgelist[-5:]
        return edgelist

    

    # Create an edge bunch from the node_property dict
    def create_nbunch_from_idpropval(self, nid_prop_val):
        nbunch = [0 for i in range(len(nid_prop_val))]

        i = 0
        for (nid, prop_val) in nid_prop_val.iteritems():
            nbunch[i] = (nid, prop_val)
            i += 1
        return nbunch

    # Create an edge bunch from the edgelist, import properties from edge_property dict
    def create_ebunch_from_idpropval_edgelist(self, eid_prop_val, edgelist, weighted=False):
            ebunch = [0 for i in range(len(edgelist))]

            i = 0
            for (eid, source, target) in edgelist:
                prop_val = eid_prop_val[eid]
                ebunch[i] = (source, target, prop_val)
                i += 1
            return ebunch



if __name__ == '__main__':
    unittest.main()
    
