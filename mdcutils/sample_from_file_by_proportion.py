# This script produces a subset of a file by sampling every Nth line in the case of a sample factor > 1
# Alternatively, for a sample_factor < 1, produces a random sample of the file proportionate to the value of the sample factor.


from mdcutils.simple_progress import ProgressMeter
import os, sys
from random import random


if __name__ == "__main__":
    
    from optparse import OptionParser
    parser = OptionParser()
    
    parser.add_option("-i", "--infile", help="File from which to sample.", 
                      type="str", dest="infile" )                 
    parser.add_option("-o", "--outfile", help="Output location.", 
                      type="str", dest="outfile"  ) 
    parser.add_option("-s", "--sample_factor", help="If < 1: Percentage=o sample of file. If > 1: Modulo operator that must be matched for each line.", 
                  type="float", dest="sample_factor", default=10 )
                  
    options, args = parser.parse_args(sys.argv[1:])
    
    sample_factor = options.sample_factor
    infile = options.infile
    outfile = options.outfile

    i = 0
    pm = ProgressMeter(999999999)    
    
    with open(infile) as fin:
        with open(outfile, 'w') as fout:
            for line in fin:
                line = line.strip()
                # Line-by-line sample
                if sample_factor >= 1.0:
                    if i % sample_factor == 0:
                        print >> fout, line
                
                # Random sample
                if sample_factor < 1.0:
                    rand = random()
                    if rand <= sample_factor:
                        print >> fout, line
                        
                pm.update()
                i += 1    
        print "Wrote to: %s" % outfile