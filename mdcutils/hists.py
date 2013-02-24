from mdcutils.simple_progress import ProgressMeter
from mdcutils.utils import sortdictbyval

import cPickle as pickle
from collections import defaultdict 

import numpy as np
from scipy import stats

import os
import math
import sys


def center(x):
    y = [[]]
    for i in range(1, len(x)):
        y.append((x[i] - x[i-1]) / 2.0 + x[i-1])
    return y

def get_edges_for_range(mn, mx, numbins):
    edges = [0 for i in range(numbins + 1)]
    binwidth = (mx-mn) / float(numbins)
    edges[0] = mn
    for i in range(0, numbins):
        edges[i+1] = mn + i*binwidth + float(binwidth)
    return edges



def get_common_bounds(a_dist, b_dist):
    a_mx, a_mn = max(a_dist), min(a_dist)
    b_mx, b_mn = max(b_dist), min(b_dist)
    
    print "Ax: %s\tAn: %s\tBx: %s\tBm: %s" % (a_mx, a_mn, b_mx, b_mn)
    # Determine Range
    mx, mn = 0,0
    if a_mx >= b_mx:    mx = a_mx
    else:               mx = b_mx
    if a_mn <= b_mn:    mn = a_mn
    else:               mn = b_mn
    bounds = (mn, mx)
    print "Bounds: %s, %s" % bounds
    return bounds
    
# This produces paired histograms with a common set of bin centers
def common_bins_ab_loghist_dump(a_dist, b_dist, base, verbose=False):
            
    bounds = get_common_bounds(a_dist, b_dist)
    
    print "A"
    a_h = log_bin_hist.for_values(a_dist_nz, base, bounds=bounds)
    print "B"
    b_h = log_bin_hist.for_values(b_dist_nz, base, bounds=bounds)
    return(a_h, b_h)

# This produces paired histograms with a common set of bin centers
def common_bins_ab_conthist_dump(a_dist, b_dist, numbins, verbose=False):
    # Get Common Bounds
    bounds = get_common_bounds(a_dist, b_dist)
    
    # Get range common to both
    mn, mx = min(a_dist), max(a_dist)
    if min(b_dist) < mn: mn = min(b_dist) 
    if max(b_dist) > mx: mx = max(b_dist)
    
    edges = get_edges_for_range(mn, mx, numbins)
                    
    a_h = np.histogram(a_dist, bins=edges)
    b_h = np.histogram(b_dist, bins=edges)
    
    return (a_h, b_h)

# Normalize vector dist cell-wise by base (dist[i] / base[i])
def norm(dist, base):
    normed = [0 for i in range(len(dist))]
    for i in range(len(dist)):
        if base[i] != 0:
            normed[i] = dist[i] / float(base[i])
    return normed
    

## Output
def dump_common_bins_ab_hist(a_h, b_h, outdir, key):    
    outfile = "%s%s.tsv" % (outdir, key)
    
    centers = center(a_h[1])
    a_v = a_h[0]
    b_v = b_h[0]
    
    print "Len Cent: %s \t Len V: %s\tLen Edges: %s" % (len(centers), len(a_v), len(a_h[1]))
    
    with open(outfile, 'w') as fout:
        print >> fout, "#center\ta_value\tb_value"
        for i in range(len(centers) - 1):
            print >> fout, "%s\t%s\t%s" % (centers[i], a_v[i], b_v[i])



            
  
    
def dump_np_hist(hist, outdir, key, verbose=False):    
    counts = hist[0]
    centers = center(hist[1])
    
    outfile = "%s%s.tsv" % (outdir, key)
    with open(outfile, 'w') as fout:
        print >> fout, "#center\tcount"
        for i in range(len(centers) -1 ):
            print >> fout, "%s\t%s" % (centers[i], counts[i] )
    
    if verbose: print "Dumped to %s" % outfile
    
    
    
def get_log_bins(vals, base):
    mn, mx = min(vals), max(vals)
    
    max_exp = math.log(mx, base)
    min_exp = math.log(mn, base)
    
    bins = []
    for i in range(int(math.floor(min_exp)), int(math.ceil(max_exp)) + 1, 1):
        bins.append(base**i)
    
    return bins
    



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
    
def dump_dists_by_prefix(prefix, relfreq, statsfile, dists_a, dists_b):
    # Small value to ensure we capture all values in range
    eps = .000000001
    
    # Standard Distributions
    with open(statsfile, 'w') as fout:
        print >> fout, "target_dist\ttotal\tmean\tmedian\tnumzeros"
        numbins = 1000
        #target_dists = ['dist_tweets', 'dist_issue_tweets', 'dist_url_tweets', 'dist_political_tweets', 'dist_political_issue_tweets', 'dist_political_url_tweets']
        target_dists = ['dist_url_tweets', 'dist_political_url_tweets']
        
        for target_dist in target_dists:
            if relfreq:
                key = "%s_%s_relfreq" % (prefix, target_dist)
            else:
                key = "%s_%s" % (prefix, target_dist)
            
            dist_a = dists_a[target_dist]
            dist_filt_a = [v for v in dist_a if v > 0]
            
            dist_b = dists_b[target_dist]
            dist_filt_b = [v for v in dist_b if v > 0]
            
            # Get range common to both
            mn, mx = min(dist_filt_a), max(dist_filt_a)
            if min(dist_filt_b) < min(dist_filt_a): mn = min(dist_filt_b) 
            if max(dist_filt_b) > max(dist_filt_a): mx = max(dist_filt_b)
                        
            edges = get_edges_for_range(mn, mx+eps, numbins)
            
            dist = []
            if prefix == 'A': dist = dist_a
            if prefix == 'B': dist = dist_b
            dist_filt = [v for v in dist if v > 0]
                            
            (counts, edges) = np.histogram(dist_filt, bins=edges)
            
            # Normalize frequencies to relative frequencies
            if relfreq:
                sum_counts = float(sum(counts))
                counts = [v / sum_counts for v in counts]
                
            dump_np_hist(counts, edges, key, True)
            
            print >> fout, "%s\t%s\t%s\t%s\t%s\t" % (target_dist, sum(dist), np.mean(dist), np.median(dist), len(dist) - len(dist_filt))
    
        # Normalized Distributions
        #target_dists = ['norm_dist_issue_tweets', 'norm_dist_url_tweets', 'norm_dist_political_tweets', 'norm_dist_political_issue_tweets', 'norm_dist_political_url_tweets']
        target_dists = ['norm_dist_url_tweets', 'norm_dist_political_url_tweets']
        for target_dist in target_dists:
            if relfreq:
                key = "%s_%s_relfreq" % (prefix, target_dist)
            else:
                key = "%s_%s" % (prefix, target_dist)
            
            dist_a = dists_a[target_dist]
            dist_b = dists_b[target_dist]
  
            dist = []
            if prefix == 'A': dist = dist_a
            if prefix == 'B': dist = dist_b
            
            bins = frange(0.0, 1.06, .05)
            (counts, edges) = np.histogram(dist, bins)
            
            # Normalize frequencies to relative frequencies
            if relfreq:
                sum_counts = float(sum(counts))
                counts = [v / sum_counts for v in counts]
            
            dump_np_hist(counts, edges, key, True)
        
            print >> fout, "%s\t%s\t%s\t%s\t%s\t" % (target_dist, sum(dist), np.mean(dist), np.median(dist), len(dist) - len(dist_filt))
