#!/usr/bin/env python
# encoding: utf-8
"""
supplemnt_nodeprop_flatfile.py

Created by Conover, Michael D on 2012-05-02.

This script will supplement a primary node property file with property values 
from a secondary node property file.  The keys of the secondary file MUST be a formal superset 
of the keys of the primary node property file.

"""

import sys

# Error for having inconsistent keysets in property files
class MissingKeys(Exception):
    def __init__(self, value=None):
        self.value = value
    def __str__(self):
        return repr(self.value)

import os, sys
from phyllotaxis.graph_tools.graph_factories import read_properties_file
from phyllotaxis.mdcutils.simple_progress import SimpleProgressMeter

def main(infile_a, infile_b, outfile, delim_p="\t", delim_s="\t", nullstr="#%"):
    print "Reading property files."
    print "\tPrimary"
    ida_prop_val = read_properties_file(infile_a, delim_p)
    print "\tSecondary"
    idb_prop_val = read_properties_file(infile_b, delim_s)
    
    ida_keys = set(ida_prop_val.keys())
    idb_keys = set(idb_prop_val.keys())
    
    print "Keys in A: %s" % len(ida_keys)
    print "Keys in B: %s" % len(idb_keys)
    
    # Ensure that the supplementary node property file is a superset of the primary file
    keyint = ida_keys.intersection(idb_keys)
    if len(keyint) != len(ida_keys):
        print "Found %s / %s primary keys not present in supplementary file." % (len(ida_keys.difference(keyint)), len(ida_keys))
        

    ida_propstrs = ida_prop_val[ida_prop_val.keys()[0]].keys()
    idb_propstrs = idb_prop_val[idb_prop_val.keys()[0]].keys()
    
    missing_prop_count = 0
    missing_userb_count = 0

    with open(outfile, 'w') as fout:
        header = ["nid"]
        propstrs = set(ida_propstrs).union(set(idb_propstrs))
        header.extend(propstrs)
        print >> fout, "\t".join(header)
        
        for key in ida_prop_val.keys():
                        
            outstr = ''
            outstr = "%s\t" % key
            
            for propstr in propstrs:
                val = nullstr
                
                if propstr in ida_prop_val[key]:
                    val = ida_prop_val[key][propstr]
                else:
                    if key in idb_prop_val:
                        if propstr in idb_prop_val[key]:
                            val = idb_prop_val[key][propstr]
                        else:
                            print "Missing %s for %s in primary and supplementary files!  Inserting nullstring." % (propstr, key) 
                            missing_prop_count += 1
                    else:
                        missing_userb_count += 1
                outstr += "%s\t" % val
                
            outstr += "\n"
           
            fout.write(outstr)
            
    print "Missing %s total property entries." % missing_prop_count
    print "Missing %s total users in File B" % missing_userb_count
    print "Wrote to: %s" % outfile

        
    

if __name__ == '__main__':
    from optparse import OptionParser
    parser = OptionParser()
    
    parser.add_option("-a", "--infile_a", help="Location of primary node property file.", 
                    type="str", dest="infile_a", default="%s" % os.environ['ANADIR'] )                 
    parser.add_option("-b", "--infile_b", help="Location of supplemtnary node property file.", 
                    type="str", dest="infile_b", default="%s" % os.environ['ANADIR'] )
    parser.add_option("-o", "--outfile", help="Location of output node property file.", 
                    type="str", dest="outfile", default="%s" % os.environ['ANADIR'] )
    parser.add_option("-p", "--delim_p", help="Delimiter for primary property file.", 
                    type="str", dest="delim_p", default="\t" )                
    parser.add_option("-s", "--delim_s", help="Delimiter for supplementary property file.", 
                    type="str", dest="delim_s", default="\t" )     
    parser.add_option("-n", "--nullstr", help="This value specifies a null string in the output property field.", 
                    type="str", dest="nullstr", default="#%" )                                                   
    options, args = parser.parse_args(sys.argv[1:])
    
    infile_a = options.infile_a
    infile_b = options.infile_b
    outfile = options.outfile
    delim_p = options.delim_p
    delim_s = options.delim_s
    nullstr = options.nullstr
    
    main(infile_a, infile_b, outfile, delim_p, delim_s, nullstr)
    
