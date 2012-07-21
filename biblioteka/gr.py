#import h
import sys
from urllib.parse import urlparse, urljoin, unquote
import pprint

c = None
dic = {}
for a in sys.stdin:
    a = a.strip()
    if not a: continue
    if '<a href' in a:
        a = a.split('<a href')[-1]
        a = a.split('</a>')[0]
        l,r = a.split('>')
        l = l.split('?')[0]
        l = l.strip( '\'"=')
        r = r.strip()
        l = unquote(l)
        print( l,':',r)
        #c[ l]= r
        assert l.split('/')[-1]== r
        c.append( l)
    elif '<p>' in a:
        c = None
    elif '<' not in a:
        c = dic[a] = []

pprint.pprint( dic)

