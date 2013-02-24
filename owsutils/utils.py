import re, string, csv, os, operator
from urlparse import urlparse
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
    
def count_lines_in_file_get_array(fname, default=0):
    count = file_len(fname)
    return [default for i in range(count - 1)]
    
def file_len(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1
    
def getStates(text):
    states = ['Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California', 'Colorado', 'Connecticut', 'Delaware', 'Florida', 'Georgia', 'Guam', 'Hawaii', 'Idaho', 'Illinois', 'Indiana', 'Iowa', 'Kansas', 'Kentucky', 'Louisiana', 'Maine', 'Maryland', 'Massachusetts', 'Michigan', 'Minnesota', 'Mississippi', 'Missouri', 'Montana', 'Nebraska', 'Nevada', 'New Jersey', 'New Mexico', 'New York', 'North Carolina', 'North Dakota', 'Ohio', 'Oklahoma', 'Oregon', 'Pennsylvania', 'Rhode', 'Island', 'South', 'Carolina', 'South', 'Dakota', 'Tennessee', 'Texas', 'Utah', 'Vermont', 'Virginia', 'Washington', 'West Virginia', 'Wisconsin', 'Wyoming']

    tweet_states = []
    for state in states:
        if text.find(state) > -1:
            tweet_states.append(1)
    return tweet_states 

def getUsernames(text):     
    hash = re.compile(r'@[a-zA-Z0-9_]+')
    return [tag.lower() for tag in hash.findall(text)]

def countUsernames(text):        
        hash = re.compile(r'@[a-zA-Z0-9_]+')
        return len(hash.findall(text))
    
def getHashtags(text):     
    hash = re.compile(r'#[a-zA-Z0-9_]+')
    return [tag.lower() for tag in hash.findall(text)]

def getOccupyHashtags(text):     
    hash = re.compile(r'#[a-zA-Z0-9_]+')
    return [tag for tag in hash.findall(text.lower()) if (tag.find('#occupy') > -1 or tag.find('#ows') > -1)]

def countHashtags(text):        
    hash = re.compile(r'#[a-zA-Z0-9_]+')
    return len(hash.findall(text))

def countUrls(text):
    return len(getUrls(text))

def getUrls(text):
    splitted = text.split()
    urls = [token for token in splitted 
            if (token.startswith("http://"))] 
    return urls

def get_valid_tokens(text, stopwords):
    text = text.strip().split()
    tokens = []
    for tok in text:
        tok = tok.lower()        
        if tok.find('#') == -1 and tok not in stopwords and tok.find("@") == -1 and tok.find("http://") == -1:
            tok = re.sub(r'\W+', '', tok)
            if tok != '':
                tokens.append(tok)
    return tokens

def read_csv(infile):
    csvfile = open(infile, "rb")

    sample = csvfile.read(1024)
    dialect = csv.Sniffer().sniff(sample)

    reader = csv.reader(csvfile, dialect)

    csvfile.seek(0)
    if csv.Sniffer().has_header(sample):
        reader.next()

    return reader 

def normalize_url(url):
    """returns the given url, normalized to domain.ext"""
    parse_object = urlparse(url)

    #remove http://
    url = parse_object.netloc

    #remove www.
    if url.startswith("www."):
        url = url[4:]

    #remove subdomain.
    pieces = url.split(".")
    if len(pieces) > 2:
        url = string.join(pieces, ".")

    return url

def get_idx_tag_freq(tseries):
    idx_tag_freq = {}
    idx = 0

    for tups in tseries:
        idx_tag_freq[idx] = defaultdict(int)

        for tup in tups:
            tweet = tup[1]
            tags = getHashtags(tweet.text)
            for tag in tags:
                idx_tag_freq[idx][tag] += 1        
        idx = idx + 1

    return idx_tag_freq

