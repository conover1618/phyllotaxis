# Remove previous HDFS network files
hdfs -rmr analysis/ows/ows_*

# Generate network flat files
pig -f gen_retweet_network_flatfiles.pig -m ./param/gen_retweet_network_flatfiles.prop

# Drop files to disk from HDFS
hdfs -cat /user/midconov/analysis/ows/ows_retweet.edgelist/p* > ~/anatwit/ows/ows_retweet.edgelist
hdfs -cat /user/midconov/analysis/ows/ows_retweet.nodeprop/p* > ~/anatwit/ows/ows_retweet.nodeprop
hdfs -cat /user/midconov/analysis/ows/ows_retweet.edgeprop/p* > ~/anatwit/ows/ows_retweet.edgeprop

# Append header data to network files

# status AS eid, status AS status, time AS ts;
echo -e "eid\tstatus\tts" > ows_retweet.edgeprop.head
cat ows_retweet.edgeprop >> ows_retweet.edgeprop.head
mv ows_retweet.edgeprop.head ows_retweet.edgeprop

# status AS eid, retweet_user AS source, screen_name AS target;
echo -e "eid\tsource\ttarget" > ows_retweet.edgelist.head
cat ows_retweet.edgelist >> ows_retweet.edgelist.head
mv ows_retweet.edgelist.head ows_retweet.edgelist

# group AS nodeid, group AS sn, iu.cnets.mdc.hadoop.twitter.MostCommonString(unq_locs) AS mode_loc
echo -e "nid\tsn\tlocstr" > ows_retweet.nodeprop.head
cat ows_retweet.nodeprop >> ows_retweet.nodeprop.head
mv ows_retweet.nodeprop.head ows_retweet.nodeprop