from collections import defaultdict 
from mdcutils.utils import sortdictbyval
from scipy import stats
import numpy as np
import math
import sys, os


###### OUTPUT

# Writes x-y values to file
# Does not need header
def dump_xy(x, y, outfile, header="centers, counts", verbose=False):    
    with open(outfile, 'w') as fout:
        print >> fout, "#%s" % header
        for i in range(len(x) -1):
            print >> fout, "%s\t%s" % (x[i], y[i])
    
    if verbose: print "Wrote to %s" % outfile

def dump_tups(tuples, outfile, header="-", verbose=False):    
    with open(outfile, 'w') as fout:
        print >> fout, "#%s" % header
        for tup in tuples:
            print >> fout, "%s\t%s\t%s" % tup
    
    if verbose: print "Wrote to %s" % outfile


def output_ints(intlist, outfile):    
    bins = [i for i in range(max(intlist) + 2)]
    (counts, redges) = np.histogram(intlist, bins)
    rel_counts =  relative_counts(counts)

    tuples = []
    for i in range(len(counts)):
        tup = (redges[i], counts[i], rel_counts[i])
        tuples.append(tup)

    dump_tups(tuples, header='redge\tcount\trel_count', outfile=outfile)

###### HISTOGRAMS

# Computes the centers between values of x
# Returns list of len(x)-1 elements
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

# Returns a list of values where each value represents 
# the proportion of the sum of the list it accounts for.
def relative_counts(counts):
    vals = []
    sum_counts = float(sum(counts))
    for count in counts:
        vals.append(count / sum_counts)
    return vals
    
def get_redges_for_range(mn, mx, numbins):
    redges = [0 for i in range(numbins)]
    binwidth = (mx-mn) / float(numbins)
    
    for i in range(numbins):
        redges[i] = mn + i*binwidth + float(binwidth)
    return redges


def frange(start, end=None, inc=None):
    "A range function, that does accept float increments..."

    if end == None:
        end = start + 0.0
        start = 0.0
    else: start += 0.0 # force it to be a float

    if inc == None:
        inc = 1.0

    count = int((end - start) / inc)
    if start + count * inc != end:
        # need to adjust the count.
        # AFAIKT, it always comes up one short.
        count += 1

    L = [None,] * count
    for i in xrange(count):
        L[i] = start + i * inc

    return L
    
    

#bins = get_log_bins(a_dist, 2)
#bins = get_bins_for_range(min(dist_filt), max(dist_filt), numbins)

#bins = numbins
#(counts, edges) = np.histogram(dist_filt, bins)