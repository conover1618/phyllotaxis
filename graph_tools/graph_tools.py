#!/usr/bin/env python
# encoding: utf-8
"""
graph_tools.py

Created by Conover, Michael D on 2012-04-30.

Generic utilities for performing functions on networkx graph objects.
"""

import sys
import os
import unittest
import networkx as nx

def remove_loops(g):
    for n in g.nodes():
        try:
            g.remove_edge(n, n)
        except(nx.NetworkXError):
            pass
    return g

def convert_multi_to_simple(g, directed=False):
    new_g = nx.Graph()
    if directed:
        new_g = nx.DiGraph()
    
    for e in g.edges(data=True):
        new_g.add_edge(e[0], e[1], e[2])
    
    return new_g


# Convert a MultiGraph into a regular graph with edges weighted according 
# to the number of edges in the source multigraph
def convert_to_multiweighted(mg, directed=False, weighted=True):
    g = None
    if directed:
        g = nx.DiGraph()
    else:
        g = nx.Graph()
    print "Creating Graph"
    for nid_a, nbrs in mg.adjacency_iter():
        for nid_b, edict in nbrs.items():
            num_edges = len(edict)
            if weighted:
                print "%s\t%s\t%s" % (nid_a, nid_b, num_edges)
                g.add_edge(nid_a, nid_b, weight=num_edges)
            else:
                g.add_edge(nid_a, nid_b)
    # Copy node properties
    for (nid, prop_val) in mg.nodes(data=True):
        g.node[nid] = prop_val
    return g
    
# Multiscale Backbone Extraction (thx yyahn@indiana) 
def extract_backbone(g, alpha):
   keep_graph = nx.Graph()
   for n in g:
       k_n = len(g[n])
       if k_n > 1:
           sum_w = sum( g[n][nj]['weight'] for nj in g[n] )
           for nj in g[n]:
               weight = g[n][nj]['weight']
               pij = 1.0*weight/sum_w
               if (1-pij)**(k_n-1) < alpha: 
                   keep_graph.add_edge( n,nj, {'weight': weight})
                   print "Adding Edge: %s\t%s\t%s" % (n,nj,weight)
   return keep_graph


def get_largest_connected_component(g):
    return nx.connected_component_subgraphs(g)[0]
