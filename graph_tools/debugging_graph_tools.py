
for nid in simple_g.nodes():
	i = simple_g.in_degree([nid]).values()[0]
	o = simple_g.out_degree([nid]).values()[0]
	if i == 0 and o == 0:
		print "%s\t%s\t%s" % (nid, i, o)



indeg = simple_g.in_degree().values()
instr = simple_g.in_degree(weighted=True).values()

outdeg = simple_g.out_degree().values()               
outstr = simple_g.out_degree(weighted=True).values()


with open('/tmp/islam19-indeg.csv', 'w') as fout:
	for deg in indeg:
		print >> fout, "%s" % deg
		
with open('/tmp/islam19-outdeg.csv', 'w') as fout:
	for deg in outdeg:
		print >> fout, "%s" % deg
		
		

# Identify min / max for timestep
import datetime
statuses = set()
mints = 9999999999999
maxts = -1
for e in g.edges(data=True):
	attr = e[2]
	ts = int(attr['ts'])
	if ts < mints:
		mints = ts
	if ts > maxts:
		maxts = ts
	statuses.add(int(attr['status']))


from owsutils.tweet_factories import BasicDiskTweetFactory

tweet_statuses = set()
filename = '/home/gfs/cnets/research/mdc/data/twitter/tweets/sergey/islam.dat.gz'
tf = BasicDiskTweetFactory(filename)
for t in tf.get_tweets():
	try:
		time = t.time
		if time <= maxts and time >= mints and t.retweet_user != '':
			tweet_statuses.add(t.status)
	except(AttributeError):
		print "Attr Error"


diff = statuses.difference(tweet_statuses)
inter = statuses.intersection(tweet_statuses)


print("Min: %s" % datetime.datetime.fromtimestamp(int(mints)).strftime('%Y-%m-%d %H:%M:%S'))
print("Max: %s" % datetime.datetime.fromtimestamp(int(maxts)).strftime('%Y-%m-%d %H:%M:%S'))


