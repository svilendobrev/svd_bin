#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from prikazki import info, DictAttr, optz, razdeli_kamila2

opts2 = DictAttr(
    yaml=   True,
#    html_index= 'aaab.tmp',
    bez=    '0',
    simvolni= True,
    dve_niva= True,
    sykr=   '../abbr',
    prevodi_meta=   '../meta_prevodi',
#    debug='items',
    vnosa_e_obiknoven= True,
#    davai =True,
#    debug='items',
)

if __name__ == '__main__':
    from indexer import indexer
    indexer._aspect2fieldtype= dict(
        zaglavie= indexer.ngram, #text,
        avtor= indexer.ngram, #text,
        )

    import sys
    optz.str( 'tyrsi',     help= 'търси в поле=стойност; полета: '+str(indexer._aspect2fieldtype.keys()) )
    info.main( opts2, sys.argv[1:] or ['.'] )

    ix = indexer()

    parcheta = []
    for x in info.vse.values():
        if x.etiketi.koren: continue
        parcheta.append( DictAttr(
            fname       = x.fname,
            zaglavie    = x.ime,
            avtor       = ', '.join( razdeli_kamila2(a) for a in x.etiketi.avtor) , #html4index
            dir         = True
            ))
        #if len(parcheta)>5:
        #    break
    if parcheta:
        for asp,idx in ix.indexes.items(): #'zaglavie', 'avtor':
            #with idx:
                i = [dict( id= p.fname, value= p.get(asp)) for p in parcheta ]
                print( i)
                idx.update( i)#[dict( id= p.fname, value= p.get(asp)) for p in parcheta ])

    if info.options.tyrsi:
        k,v = info.options.tyrsi.split('=')
        idx = getattr( ix.indexes, k)
        #or use FuzzyTermPlugin
        s = idx.searcher

        MAXDIST = 2
        PREFIX =  0

        #from whoosh import fields, index,

        from whoosh import query
        #qparser.FuzzyTermPlugin hooks direct to query.FuzzyTerm, so replacing that is too late
        qft__init__ = query.FuzzyTerm.__init__
        def __init__(self, fieldname, text, boost=1.0, maxdist=1,
                        prefixlength= PREFIX, constantscore=True):
                 qft__init__( **locals())
        query.FuzzyTerm.__init__ = __init__

        from whoosh import qparser #  , analysis
        #ocreate = qparser.FuzzyTermPlugin.create
        def create(self, parser, match):
                mdstr = match.group("maxdist")
                maxdist = int(mdstr) if mdstr else MAXDIST

                pstr = match.group("prefix")
                prefix = int(pstr) if pstr else PREFIX

                #print( 111111, locals())
                return self.FuzzinessNode(maxdist, prefix, match.group(0))
        qparser.FuzzyTermPlugin.create = create


        if 0:
            class OrGroup( qparser.OrGroup):
                def __init__( self, *a,**ka):
                    #print ( 11111111111, a, ka)
                    ka.setdefault( 'scale', 0.9)
                    return super().__init__( *a,**ka)
                    return super().__init__( scale= ka.pop( 'scale', 0.9), *a,**ka)

            #FIX omissions:
            from whoosh import matching
            def _replacement(self, newchild):
                return self.__class__(newchild, scale=self._scale)
            matching.CoordMatcher._replacement = _replacement


        qp = qparser.QueryParser( 'value',
        #p = qparser.MultifieldParser( ('value', 'ngram'),
                schema= idx.ix.schema,
                #group= qparser.OrGroup #.factory(0.9), # a b -> both a and b better than a and a
            )

        qp.add_plugin( qparser.FuzzyTermPlugin())
        #from whoosh.query import FuzzyTerm
        #r = s.search( FuzzyTerm( 'value', v, maxdist=4, prefixlength=0 ), limit=None)
        #r = idx.find( v, limit=None, exact=False, maxdist=3)

        r = s.search( qp.parse( v ), limit=None)
        #print( r)
        print( ':::::::')
        for l in r:
            print( l.score, l.fields()['value'])

# vim:ts=4:sw=4:expandtab
