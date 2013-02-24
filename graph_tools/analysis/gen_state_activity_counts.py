#!/usr/bin/env python
# encoding: utf-8
"""
gen_state_activity_counts.py

Created by Conover, Michael D on 2012-06-04.

This script ..
"""

import os, sys

def main():
    pass

if __name__ == '__main__':
    from optparse import OptionParser
    parser = OptionParser()
    
    parser.add_option("-i", "--infile", help="Location of input file.", 
                    type="str", dest="infile", default="%stwitter/foo.in" % os.environ['ANADIR'] )                 
    parser.add_option("-o", "--outfile", help="Location of output file.", 
                    type="str", dest="outfile", default="%stwitter/foo.out" % os.environ['ANADIR'] )
    # parser.add_option("-v", "--verbose", help="Allow verbose output.", 
    #                dest="verbose", action="store_true")                                    
    options, args = parser.parse_args(sys.argv[1:])
    
    infile = options.infile
    outfile = options.outfile
    
    main()
    
