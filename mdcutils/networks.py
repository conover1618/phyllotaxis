import igraph as ig
from collections import defaultdict
from mdcutils.simple_progress import ProgressMeter

def copyGraphAttributes_AtoB(A, B):
        for attr in A.attributes():
            B[attr] = A[attr]
        return B

def convertToBiggestCC(g):        
        ccs = g.components(ig.WEAK)
        idx_of_biggest_cc, size_of_biggest_cc = max(enumerate([len(x) for x in ccs]), key=lambda x: x[1])    
        biggest_cc = ccs.subgraph(idx_of_biggest_cc)        
        biggest_cc = copyGraphAttributes_AtoB(g, biggest_cc)        
        g['biggest_cc'] = True
        
        return biggest_cc
        
        
# Consumes a list of tuples into an igraph object
def convert_edgelist_to_igraph(edgelist):
    # Count & Track Nodes
    nodeid_idx = {}
    nodeidx_id = {}
    nodeidx = 0
    for e in edgelist:
        source, target = e[0], e[1]
        
        for nodeid in [source, target]:
            if nodeid not in nodeid_idx:
                nodeid_idx[nodeid] = nodeidx
                nodeidx_id[nodeidx] = nodeid
                nodeidx += 1
    g = ig.Graph()
    edge_weight = defaultdict(int)
    for i in range(len(edgelist)):
        e = edgelist[i]
        
        a = nodeid_idx[e[0]]
        b = nodeid_idx[e[1]]        
        
        edge_weight[(a, b)] += 1
        edge_weight[(b, a)] += 1
    edges = []
    weights = []
    for (edge, weight) in edge_weight.items():
        edges.append(edge)
        weights.append(weight)
    g.add_edges(edges)
    g.es['Weight'] = weights
    
    attr_id = [nodeidx_id[idx] for idx in range(len(g.vs))]
    g.vs['id'] = attr_id
    return g
    


def build_graph_from_dirid_bexorgs(dirid_bexorgs):
    nodeid_idx = {}
    nodeidx_id = {}
    nodeidx = 0
    for bexorg in dirid_bexorgs.keys():
        nodeid_idx[bexorg] = nodeidx
        nodeidx_id[nodeidx] = bexorg
        nodeidx += 1
    edges = []
    for (dirid, bexorgs) in dirid_bexorgs.items():
        bexorgs = list(bexorgs)
        for i in range(len(bexorgs)):
            for j in range(i):
                b1 = nodeid_idx[bexorgs[i]]
                b2 = nodeid_idx[bexorgs[j]]
                
                edges.append((b1, b2))
    print edges
    g = convert_edgelist_to_igraph(edges)   
    return g
                
                
    
# GARBAGE DELETE
def build_graph_from_bexorg_dirids(bexorg_dirids):
    pm = ProgressMeter(len(bexorg_dirids))
    edge_weight = {}
    nodeid_idx = {}
    nodeidx_id = {}
    nodeidx = 0
    for bexorg in bexorg_dirids.keys():
        nodeid_idx[bexorg] = nodeidx
        nodeidx_id[nodeidx] = bexorg
        nodeidx += 1
    
    keys = bexorg_dirids.keys()
    for i in range(len(keys)):
        for j in range(len(keys)):
            if i < j:
                bex1 = keys[i]
                bex2 = keys[j]
                if bex1 != bex2:
                    bex1_dirs = set(bexorg_dirids[bex1])
                    bex2_dirs = set(bexorg_dirids[bex2])
                    inter = len(bex1_dirs.intersection(bex2_dirs))
                    union = len(bex1_dirs) + len(bex2_dirs) - inter
                    
                    bex1_idx = nodeid_idx[bex1]
                    bex2_idx = nodeid_idx[bex2]
                    
                    edge_weight[(bex1_idx, bex2_idx)] = inter / float(union)
        pm.update()  
    edges = []
    weights = []
    for (edge, weight) in edge_weight.items():
        edges.append(edge)
        weights.append(weight)
    
    g = ig.Graph()
    g.add_edges(edges)
    g.es['Weight'] = weights
    
    return g
        
# Creates a bipartite graph from an edgelist (member, group) based on co-membership
# direction: controls which side of the edgelist (left, right) we are projecting onto
#   for example, a left projection on an edgelist with person -> company
#   would project a network of people based on company co-membership
#   where 'right' would produce a network of companies based on shared employees

def get_bi_partite_projection_edgelist(edgelist, direction='left'):
    assoc = defaultdict(set)

        
    # Aggregate all members of each group
    for e in edgelist:
        group = None
        member = None
        
    
        if direction=='left':
            group = e[1]
            member = e[0]
        if direction=='right':
            group = e[0]
            member = e[1]
        
        assoc[group].add(member)
    
    projection_edgelist = []

    # Draw relations between all pairs members of each group
    for (group, members) in assoc.items():
        members = list(members)
        for i in range(len(members)):
            for j in range(i):
                m1 = members[i]
                m2 = members[j]
                
                projection_edgelist.append((m1, m2))
    
    
    
    return list(projection_edgeset)
  

# Assigns attributes to a graph based on a map from nodeids -> attribute value
def assign_node_attributes(g, attrkey, nodeid_attr, defaultval=0):
    
    # Create nodeidx -> id map
    nodeid_idx = {}
    nodeidx_id = {}
    
    idx = 0
    for id in g.vs['id']:
        nodeid_idx[id] = idx
        nodeidx_id[idx] = id
        idx += 1
        
    attrs = [defaultval for i in range(len(g.vs))]
    for i in range(len(g.vs)):
        id = nodeidx_id[i]
        if id in nodeid_attr:
            val = nodeid_attr[id]
            attrs[i] = val
    
    g.vs[attrkey] = attrs
    
    return g
    
          
if __name__ == "__main__":
    # Bipartite
    edgelist = [(1, 'a'), (1,'b'), (1,'c'), (2,'a'), (3,'b'), (3,'c'), (4, 'c'), (5,'d'), (6, 'd')]
    g = bi_partite_projection(edgelist, direction='right')
    print g
    
    # Edgelist
    bp_edgelist = get_bi_partite_projection_edgelist(edgelist, directed=True)
    print convert_edgelist_to_igraph(bp_edgelist, direction='right')
    
    