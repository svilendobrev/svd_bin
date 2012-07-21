#$Id$

'''help = 'merge two .toc, copying CD_TEXT
from the CD_TEXT-having into the CD_TEXT-less. assumes same number tracks
e.g. .toc with separate files (w/ CD_TEXT), and a .toc from made CD as single image (w/o CD_TEXT)'
'''
import sys,re
re_cdtext = re.compile( '\s+(CD_TEXT\s*\{[\s\S]*?\} *\})' )
re_flags = re.compile( '^((NO\s+)?(COPY|PRE_EMPHASIS)|TWO_CHANNEL_AUDIO|FOUR_CHANNEL_AUDIO|ISRC)')

args = sys.argv[1:]
assert len(args)>=2, help
#fa = file( args[0]).read()
#fb = file( args[1]).read()
track = 'TRACK AUDIO'
la,lb = ( file(name).read().strip().split( track) for name in args[:2] )
assert len(la) == len(lb)
ba = None
r = []
for a,b in zip( la,lb):
    if ba is None:
        ba = 'CD_TEXT' in b
        assert ba == ('CD_TEXT' not in a)
    if ba: b,a=a,b
    m = re_cdtext.search( a)
    assert m
    cdtxt = m.group(1)
    lines = [ x.strip() for x in b.split('\n') ]
    if lines[0].startswith( 'CD_DA'): #hdr
        lines.insert( 1, cdtxt )
    else:   #track
        for n,l in enumerate( lines):
            if l and not re_flags.search( l): break
        lines.insert( n, cdtxt)

    bb = '\n  '.join( lines).rstrip()+'\n'
    r.append( bb )

print track.join( r )
# vim:ts=4:sw=4:expandtab
