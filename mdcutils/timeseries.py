import math
from datetime import *
import os, sys

# Sort objects into timeseries bins based on timestamp tuple with form (ts, object)
# object in each bin is the original tuple

def create_object_timeseries(timestamp_tuples, resolution, sliding_step=-1, start_ts=-1, end_ts=-1):
    timestamps = [tup[0] for tup in timestamp_tuples]
    
    
    resolution = float(resolution)
    
    if start_ts == -1:
        min_ts = min(timestamps)
    if end_ts == -1:
        max_ts = max(timestamps)
    
    if start_ts != -1:
        min_ts = start_ts
    if end_ts != -1:
        max_ts = end_ts
    
    series = []
    if sliding_step > -1:
        tslen = math.ceil(max_ts + .000001 - min_ts)
        #numbins = int( (tslen / resolution) * sliding_step) + 1
        
        numbins = int( (tslen - resolution) / sliding_step) + 1
        
        #print "Max TS:\t%s" % max_ts
        #print "Min TS:\t%s" % min_ts
        #print "Len:\t%s" % tslen
        #print "Step:\t%s" % sliding_step
        #print "Res:\t%s" % resolution
        #print "Bins:\t%s" % numbins
        
  
        series = [[] for i in range(numbins)]
        
        for tup in timestamp_tuples:
            ts = tup[0]
            if ts >= min_ts and ts <= max_ts:
                mxbinidx = (ts - min_ts) - resolution 
                
                lower_ts = ts - resolution
                upper_ts = ts + resolution
                
                if upper_ts > max_ts - resolution: 
                    upper_ts = max_ts - resolution
                if lower_ts < min_ts:
                    lower_ts = min_ts           
                
                ts_range = range(lower_ts, upper_ts, sliding_step)
                binidxs = [int((val - min_ts) / sliding_step) for val in ts_range]
    
                
                for binidx in binidxs:
                    series[binidx].append(tup) 
                    #print "Appenfing to: %s" % binidx       

    else:
        numbins = int(math.ceil((max_ts + .000001 - min_ts) / resolution))
        series = [[] for i in range(numbins)]
        for tup in timestamp_tuples:
            ts = tup[0]
            if ts >= min_ts and ts <= max_ts:
                binidx = int((ts - min_ts) / resolution)
                series[binidx].append(tup)

    
    return series
    

    

# Aggregate just timestamps by bin, return dict of binidx -> [timestamp_list]
def create_timeseries(timestamps, resolution, start_ts=-1, end_ts=-1):
    resolution = float(resolution)
    
    if start_ts == -1:
        min_ts = min(timestamps)
    if end_ts == -1:
        max_ts = max(timestamps)
    
    if start_ts != -1:
        min_ts = start_ts
    if end_ts != -1:
        max_ts = end_ts
    
    numbins = int(math.ceil((max_ts + .000001 - min_ts) / resolution))
    
    series = [[] for i in range(numbins)]
    
    for ts in timestamps:
        if ts >= min_ts and ts <= max_ts:
            binidx = int((ts - min_ts) / resolution)
            #print "%s : %s - %s (%s) / %s " % (binidx, ts , min_ts, ts - min_ts, resolution)
            series[binidx].append(ts)
        
    #print "Min|Max: %s | %s" % (min_ts, max_ts)
    #print "Bins: %s" % numbins
    #print counts
    
    return series

# Aggregate timestamp/weight tuples into each bin
def create_weighted_timeseries(timestamp_weight_tuples, resolution):
    resolution = float(resolution)
    
    
    # Paired lists of timestamps and weights
    timestamps = [float(tup[0]) for tup in timestamp_weight_tuples]
    weights = [float(tup[1]) for tup in timestamp_weight_tuples]
    
    min_ts = min(timestamps)
    max_ts = max(timestamps)
    
    numbins = int(math.ceil((max_ts + .000001 - min_ts) / resolution))
    
    series = [[] for i in range(numbins)]
    
    for i in range(len(timestamps)):
        ts = timestamps[i]
        weight = weights[i]
        
        binidx = int((ts - min_ts) / resolution)
        series[binidx].append((ts, weight))
    
    return series

    
    
def print_series_with_dates(series, start_ts, resolution, weighted=False):
    # Optionally pass a series containing tuples of the form timestamp/weight
    
    datestamp = datetime.fromtimestamp(start_ts)
    delta = timedelta(seconds=resolution)
    
    print "binidx\tdatestamp\tcount"
    
    for binidx in range(len(series)):
        datestr = "%s-%s-%s" % (datestamp.month, datestamp.day, datestamp.year)
        if not weighted:
            print "%s\t%s\t%s" % (binidx, datestr, len(series[binidx]))
        if weighted:
            weights = [tup[1] for tup in series[binidx]]
            print "%s\t%s\t%s" % (binidx, datestr, sum(weights))

        datestamp += delta


def write_series_with_dates(series, start_ts, resolution, outfile, weighted=False, verbose=True):
    datestamp = datetime.fromtimestamp(start_ts)
    delta = timedelta(seconds=resolution)
    
    with open(outfile, 'w') as fout:
        
        if weighted: 
            print >> fout, "binidx\tdatestamp\tweight\tavg_weight"
        if not weighted:
             print >> fout, "binidx\tdatestamp\tcount"
        
        for binidx in range(len(series)):
            datestr = "%s-%s-%s" % (datestamp.month, datestamp.day, datestamp.year)
            if not weighted:
                print >> fout, "%s\t%s\t%s" % (binidx, datestr, len(series[binidx]))
            if weighted:
                weights = [tup[1] for tup in series[binidx]]
                
                try:
                    print >> fout, "%s\t%s\t%s\t%s" % (binidx, datestr, sum(weights), sum(weights) / len(weights))
                except(ZeroDivisionError):
                    print >> fout, "%s\t%s\t%s\t%s" % (binidx, datestr, sum(weights), 0.0)
            datestamp += delta
    
    if verbose: print "Wrote to: %s" % outfile
    
  
if __name__ == "__main__":

    # Consumes a file containing timestamps or timestamp\tweight tuples (controlled by weighted option)
    # and produces a timseries file containing binidx\tdatestamp\tweight, where weight is either 
    # the count of events in this bin or the sum of the weights of the associated timestamps.
    
    
    from optparse import OptionParser
    parser = OptionParser()
    
    parser.add_option("-o", "--outfile", help="File to write bindix \t count \t datestring binned timeseries output..", 
                      type="str", dest="outfile", default="%stwitter/new_scientist/timestamps/foo_out.txt" % os.environ['ANADIR'] )
    parser.add_option("-i", "--tsfile", help="File containing timestamps to bin and count.", 
                      type="str", dest="tsfile", default="%stwitter/new_scientist/timestamps/foo_in.txt" % os.environ['ANADIR'] ) 
    parser.add_option("-r", "--resolution", help="Bin resolution in seconds.", 
                      type="int", dest="resolution", default=86400 ) 
    parser.add_option("-w", action="store_true", dest="weighted")

    options, args = parser.parse_args(sys.argv[1:])
    
    outfile = options.outfile
    tsfile = options.tsfile
    resolution = options.resolution
    weighted = options.weighted
    
    if weighted:
        raw_series = [tuple(line.strip().split()) for line in open(tsfile).readlines() if line.find("#") == -1]
        
        timestamps = [float(tup[0]) for tup in raw_series]
        
        series = create_weighted_timeseries(raw_series, resolution)
        #print_series_with_dates(series, min(timestamps), resolution, weighted=True)
        write_series_with_dates(series, min(timestamps), resolution, outfile, weighted=True)
    
    if not weighted:
        raw_series = [int(line.strip()) for line in open(tsfile).readlines() if line.find("#") == -1]
    
        series = create_timeseries(raw_series, resolution)
        #print_series_with_dates(series, min(raw_series), resolution)
        write_series_with_dates(series, min(raw_series), resolution, outfile)