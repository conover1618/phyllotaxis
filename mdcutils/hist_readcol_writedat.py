import mdcutils.proper_histograms as h
import sys
import numpy as np

if __name__ == '__main__':
    from optparse import OptionParser
    parser = OptionParser()
    
    parser.add_option("-f", "--fpath", help="Input file.", 
                      type="str", dest="fpath")    
    parser.add_option("-o", "--opath", help="Output file.", 
                      type="str", dest="opath")
    parser.add_option("-i", "--colidx", help="Column index.", 
                      type="int", dest="colidx", default=0)
    parser.add_option("-t", "--bin_type", help="Type of binning. [cont|log|int]", 
                      type="str", dest="bin_type", default="cont")
    parser.add_option("-n", "--num_bins", help="Number of bins.", 
                      type="int", dest="num_bins", default=10)                  
    parser.add_option("-v", action="store_true", dest="verbose")
                          
    options, args = parser.parse_args(sys.argv[1:])   
    fpath = options.fpath
    opath = options.opath
    colidx = options.colidx
    bin_type = options.bin_type
    num_bins = options.num_bins

    verbose = options.verbose
    

    vals = h.read_col_from_file(fpath, colidx)
    
    
    bins = num_bins
    if bin_type == 'log':
        bins = h.get_log_bins(vals, 2.0)
    if bin_type == 'int':
        bins = range(min(vals) + 1, max(vals) + 1)
    
    hist = np.histogram(vals, bins=bins)
    h.dump_np_hist(hist, opath)

    if verbose: 
        print "Read %s values from %s" % (len(vals), fpath)
        print "Wrote to:\ncat %s" % opath
    