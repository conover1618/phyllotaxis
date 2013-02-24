import simplejson
from time import mktime, strptime, localtime, strftime
import re
import codecs


class Tweet(object):
    def __init__(self, tweet_str = None, quiet = False):
    
        if tweet_str != None:
            if not quiet:
                print tweet_str.strip()

            fields = tweet_str.strip().split("|")
            
            self.user = int(fields[0]) # user id
            self.status = int(fields[1]) # tweet id
            self.time = int(fields[2]) # unix time stamp
            self.text = fields[3] # tweet contents
            self.location = fields[4] # Self reported location string
            self.source = fields[5] # Client used to generate the tweet (web interface, iphone client, etc)
            self.follow = int(fields[6]) # How many followers the user has
            self.reply_status = int(fields[7]) # id of the tweet it is replying to
            self.reply_user = fields[8] # screen_name of the user it is replying to.
            self.screen_name = None
            self.retweet_status = 0
            self.retweet_user = None
            self.lat = ""
            self.lon = ""
            
            if len(fields) > 9:
                self.screen_name = fields[9]
                
                if len(fields) > 10:
                    self.retweet_status = int(fields[10])
                    self.retweet_user = fields[11]
                
                    if len(fields) > 12:
                        self.lat = fields[12]
                        self.lon = fields[13]

        else:
            self.user = 0 # user id
            self.status = None # tweet id
            self.time = None # unix time stamp
            self.text = "" # tweet contents
            self.location = "" # Self reported location string
            self.source = "" # Client used to generate the tweet (web interface, iphone client, etc)
            self.follow = 0 # How many followers the user has
            self.reply_status = 0 # id of the tweet it is replying to
            self.reply_user = "" # screen_name of the user it is replying to.
            self.screen_name = None
            self.retweet_status = 0
            self.retweet_user = None
            self.lat = ""
            self.lon = ""

    def graph_view(self):
        return "%s -> (%s, %s) (%s)" % (
            self.screen_name, self.reply_user, self.retweet_user, self.text)
            
    def __repr__(self):
        return ("%d|%d|%d|%s|%s|%s|%s|%d|%s|%s|%d|%s|%s|%s" % (self.user, self.status, self.time, self.text, self.location, self.source, self.follow, self.reply_status, self.reply_user, self.screen_name, self.retweet_status, self.retweet_user, self.lat, self.lon)).encode('utf-8')
    
    def __repr_catch_unicode_error__(self):
        return unicode("%d|%d|%d|%s|%s|%s|%s|%d|%s|%s|%d|%s|%s|%s" % (self.user, self.status, self.time, self.text, self.location, self.source, self.follow, self.reply_status, self.reply_user, self.screen_name, self.retweet_status, self.retweet_user, self.lat, self.lon), errors='ignore')

    def __str__(self):
        return self.__repr__()

def parseTweet(t, sj=simplejson):
    tmp = Tweet()

    try:
        tweet = sj.loads(t.strip())
    except Exception, e:
        return None
        
    if "delete" in tweet:
        return None

    if "scrub_geo" in tweet:
        return None

    created_at = tweet["created_at"].split()

    tmp.user = int(tweet["user"]["id"])
    tmp.status = int(tweet["id"])
    tmp.time = int(mktime(strptime(" ".join([created_at[i] for i in xrange(6) if i!=4]), '%a %b %d %H:%M:%S %Y')))
    tmp.text = re.sub("\||\n|\t"," ", tweet["text"]) # Clean tweet text (line breaks, | and tabs)
    
    if tweet["user"]["location"] != None:
        tmp.location = re.sub("\||\n|\t"," ", tweet["user"]["location"])
    
    if tweet["source"] != None:
        tmp.source = re.sub("\||\n|\t"," ", tweet["source"]) 
        
    tmp.follow = int(tweet["user"]["followers_count"])

    if tweet["in_reply_to_status_id"] != None:
        tmp.reply_status = int(tweet["in_reply_to_status_id"])
    else:
        tmp.reply_status = 0
        
    if tweet["in_reply_to_screen_name"] != None:
        tmp.reply_user = tweet["in_reply_to_screen_name"]
    else:
        tmp.reply_user = ""

    tmp.screen_name = tweet["user"]["screen_name"]
    
    if "retweeted_status" in tweet:
        tmp.retweet_status = int(tweet["retweeted_status"]["id"])
        tmp.retweet_user = tweet["retweeted_status"]["user"]["screen_name"]
    else:
        tmp.retweet_status = 0
        tmp.retweet_user = ""

    tmp.lat = ""
    tmp.lon = ""
    
    if "geo" in tweet and tweet["geo"]:
        tmp.lat = tweet["geo"]["coordinates"][0]
        tmp.lon = tweet["geo"]["coordinates"][1]

    return tmp

def parseDataSift(t, sj=simplejson):
    tmp = Tweet()

    try:
        tweet = sj.loads(t.strip())
    except Exception, e:
        return None

    tweet = tweet["data"]

    if "delete" in tweet:
        return None

    if "scrub_geo" in tweet:
        return None

    created_at = tweet["created_at"].split()

    tmp.user = int(tweet["user"]["id"])
    tmp.status = int(tweet["id"])
    tmp.time = int(mktime(strptime(" ".join([created_at[i] for i in xrange(6) if i!=4]), '%a %b %d %H:%M:%S %Y')))
    tmp.text = re.sub("\||\n|\t"," ", tweet["text"]) # Clean tweet text (line breaks, | and tabs)

    if tweet["user"]["location"] != None:
        tmp.location = re.sub("\||\n|\t"," ", tweet["user"]["location"])

    if tweet["source"] != None:
        tmp.source = re.sub("\||\n|\t"," ", tweet["source"])

    tmp.follow = int(tweet["user"]["followers_count"])

    if tweet["in_reply_to_status_id"] != None:
        tmp.reply_status = int(tweet["in_reply_to_status_id"])
    else:
        tmp.reply_status = 0

    if tweet["in_reply_to_screen_name"] != None:
        tmp.reply_user = tweet["in_reply_to_screen_name"]
    else:
        tmp.reply_user = ""

    tmp.screen_name = tweet["user"]["screen_name"]

    if "retweeted_status" in tweet:
        tmp.retweet_status = int(tweet["retweeted_status"]["id"])
        tmp.retweet_user = tweet["retweeted_status"]["user"]["screen_name"]
    else:
        tmp.retweet_status = 0
        tmp.retweet_user = ""

    tmp.lat = ""
    tmp.lon = ""

    if "geo" in tweet and tweet["geo"]:
        tmp.lat = tweet["geo"]["coordinates"][0]
        tmp.lon = tweet["geo"]["coordinates"][1]

    return tmp


# Module-public regular expressions, compiled here for speed
tweet_scrub_regex = re.compile("\||\n|\t")
rt_regex = re.compile(r"^rt @(\w+)", re.IGNORECASE)
username_scrub_regex = re.compile(r"(?:rt )?@\S+", re.IGNORECASE)
to_regex = re.compile(r"(?<!rt )@(\w+)", re.IGNORECASE)

def parseSearch(tweet, user_ids):
    tmp = Tweet()

    if "delete" in tweet:
        return None

    if "scrub_geo" in tweet:
        return None

    created_at = tweet["created_at"].split()

    tmp.screen_name = tweet["from_user"]
    
    #if tmp.screen_name in user_ids:
    tmp.user = 0 #int(user_ids[tmp.screen_name])

    tmp.status = int(tweet["id"])

    tmp.time = int(mktime(strptime(" ".join(created_at[:-1]),
                                   '%a, %d %b %Y %H:%M:%S')))

    # Clean tweet text (line breaks, | and tabs)
    tmp.text = tweet_scrub_regex.sub(" ", tweet["text"]) 
    
    tmp.location = ""
    
    if tweet["source"] != None:
        tmp.source = tweet_scrub_regex.sub(" ", tweet["source"]) 
        
    tmp.follow = 0 #int(tweet["user"]["followers_count"])

    m = to_regex.search(tmp.text)
    if m:
        tmp.reply_user = m.group(1)
    else:
        tmp.reply_user = "" 
    
    tmp.reply_status = 0
    tmp.retweet_status = 0
    tmp.retweet_user = ""

    m = rt_regex.search(tmp.text)
    if m:
        tmp.retweet_user = m.group(1)

    # scrub retweet, reply users from tweet
    # tmp.text = username_scrub_regex.sub("", tmp.text)

    return tmp
#     if tmp.text[0:2].lower() == "rt":
#         temp = tmp.text.split()[1]
# 	if temp[0] == "@" and temp[-1] == ":":
# 	    tmp.retweet_user = temp[1:-1]
