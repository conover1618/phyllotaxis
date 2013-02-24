import re
import string
import os
import numpy as np
import operator


def sortdictbyval( dict, n, desc=True, verbose=False):
    sorted_dict = sorted(dict.iteritems(), key=operator.itemgetter(1))
    if desc: sorted_dict.reverse()
    if verbose:
        for tup in sorted_dict[:n]:
            print "\t%s\t%s" % (tup[0], tup[1])
    return sorted_dict[:n]



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