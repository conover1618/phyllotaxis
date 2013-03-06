# This script subsets a graph based on nodeids specified in an additional file

import os, sys
from phyllotaxis.mdcutils import utils

def main(inbase, outbase, nodeid_file):
    print "Reading Node Ids"
    nodeids = set([line.strip() for line in open(nodeid_file).readlines()])

    print "Read %s Node Ids" % len(nodeids)
    suffixes = ['.nodeprop', '.edgelist']
    for suffix in suffixes:
        print suffix
        outfile = "%s%s" % (outbase, suffix)
        with open(outfile, 'w') as fout:
            infile = "%s%s" % (inbase, suffix)
            

            firstline = True
            total = 0
            matched = 0

            print "Reading from: %s" % infile
            fin = open(infile)
            for line in fin:
                
                if not firstline:
                    row = line.strip().split()

                    fields = []
                    if suffix == '.nodeprop':
                        if row[0] in nodeids:
                            fout.write(line)
                            matched += 1
                            
                    if suffix == '.edgelist':
                        if row[1] in nodeids and row[2] in nodeids:
                            fout.write(line)
                            matched += 1
                            
                    total += 1
                else:
                    fout.write(line)
                    firstline = False

        print "%s / %s" % (matched, total)
        print "Wrote to: %s" % outfile 

    fin.close()
    fout.close()
    

if __name__ == "__main__":
    from optparse import OptionParser
    parser = OptionParser()
    
    parser.add_option("-i", "--inbase", help="Path to input input.", 
                    type="str", dest="inbase", default="%s/endorserank/skillgraph/foo.tsv" % os.environ['ANADIR'])                 
    parser.add_option("-o", "--outbase", help="Path to output base..", 
                    type="str", dest="outbase", default="%s/endorserank/skillgraph/gtedgelists/" % os.environ['ANADIR'])
    parser.add_option("-n", "--nodeid_file", help="List of node ids to retain.", 
                    type="str", dest="nodeid_file" )   

    options, args = parser.parse_args(sys.argv[1:])
    
    inbase = options.inbase
    outbase = options.outbase
    nodeid_file = options.nodeid_file


    main(inbase, outbase, nodeid_file)