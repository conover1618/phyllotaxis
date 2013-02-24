import numpy as np
from scipy import stats

import os
import math
import sys

# Binning

def center(x):
    y = [x[0]]
    for i in range(1, len(x)):
        y.append((x[i] - x[i-1]) / 2.0 + x[i-1])
    return y

def get_log_bins(vals, base):
    mn, mx = min(vals), max(vals)
    
    max_exp = int(math.ceil(math.log(mx, base)))
    min_exp = int(math.floor(math.log(mn, base)))
    
    bins = []
    for i in range(min_exp, max_exp + 1, 1):
        bins.append(base**i)
    
    return bins
    
    
# File Input
def read_col_from_file(fpath, colidx):
    vals = []
    with open(fpath) as fin:
        for line in fin:
            line = line.strip().split()
            val = float(line[colidx])
            vals.append(val)
    return vals
    

# File Output

def dump_np_hist(hist, opath, verbose=False):   
    height_type = 'count'
     
    heights = hist[0]
    centers = center(hist[1])
    
    with open(opath, 'w') as fout:
        print >> fout, "#center\t%s" % height_type
        for i in range(len(centers) -1 ):
            print >> fout, "%s\t%s" % (centers[i], heights[i] )
    
    if verbose: print "Wrote histogram data to %s" % outfile
    

