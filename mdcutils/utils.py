import re, string, csv, os, operator
import time
from collections import defaultdict

def _mkdir(newdir):
    """works the way a good mkdir should :)
        - already exists, silently complete
        - regular file in the way, raise an exception
        - parent directory(ies) does not exist, make them as well
    """
    if os.path.isdir(newdir):
        pass
    elif os.path.isfile(newdir):
        raise OSError("a file with the same name as the desired " \
                      "dir, '%s', already exists." % newdir)
    else:
        head, tail = os.path.split(newdir)
        if head and not os.path.isdir(head):
            _mkdir(head)
        #print "_mkdir %s" % repr(newdir)
        if tail:
            os.mkdir(newdir)
            
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
    

def count_lines_in_file_get_array(fname, default=0):
    count = file_len(fname)
    return [default for i in range(count - 1)]
    
    
def file_len(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1
    