#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function
if 0:
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

if 10:
    from whoosh import fields, index, query, qparser, analysis
    from indexer import AspectIndexer, DictAttr
    #ngram = indexer.ngram['ngram']
    #ngram = fields.NGRAM( stored=True)
    text    = fields.TEXT( analyzer= analysis.SimpleAnalyzer(), spelling=True, stored=True)
    ngram   = fields.TEXT( analyzer= analysis.NgramWordAnalyzer(2),
        #phrase=False,
        chars   = True,
        spelling= True,
        stored  = True,
        )
    #ngram става за предложения, но не става за приблизително търсене
    class aschema:
        avtor    = text #ngram
        zaglavie = text #ngram
        id = fields.ID( unique=True, stored=True)
    class IX( AspectIndexer):
        def get_alldata( me):
            return dict( (f['id'], f ) for f in me.searcher.all_stored_fields() )
        def get_value( me, a): return a
        def fix_value( me, a): pass
    schema = fields.Schema(
        id     = aschema.id,
        **dict(
            [ ('n_'+k,ngram) for k in vars(aschema) if k != 'id' and k[0]!='_' ]
            +
            [ (k,v) for k,v in vars(aschema).items() if k != 'id' and k[0]!='_' ]
        )
        )
    index_dir = 'ixx'
    ixx = IX( schema, index_dir)
    if 0:
        if os.path.exists( index_dir):
            ix = index.open_dir( index_dir)
        else:
            os.makedirs( index_dir)
            ix = index.create_in( index_dir, schema)
        searcher = ix.searcher()

    parcheta = [
        DictAttr(
            avtor   = 'avtoryt vtoroime',
            zaglavie= 'tvorbata mu',
            id= '/pyt/1/',
            ),
        DictAttr(
            avtor   = 'avtoryt vtoroimeto',
            zaglavie= 'druga tvorba',
            id= '/pyt2/file',
            ),
        DictAttr(
            avtor   = 'drug avtor',
            zaglavie= 'edna druga tvorbata mu',
            id= '/pyt3/file',
            ),
    ]

if __name__ == '__main__':
    INFO = 0
    if INFO:
        from indexer import indexer
        indexer._aspect2fieldtype= dict(
            zaglavie= indexer.ngram, #text,
            avtor= indexer.ngram, #text,
            )

    import sys
    import optz
    optz.str( 'tyrsi',     help= 'търси в поле=стойност; полета: '+str( ixx.schema._fields.keys() )) #schindexer._aspect2fieldtype.keys()) )
    optz.bool( 'novo',     help= 'Създава индекса')
    optz.bool( 'dump',     help= 'всички данни')
    optz.str( 'index',     help= 'избор на друг индекс')
    if INFO:
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
        tyrsi = info.options.tyrsi
    else:
        optz,args = optz.get()
        if not optz.tyrsi and args: optz.tyrsi = ' '.join( args)
        idx = ixx
        if optz.novo:
            print( schema)
            if parcheta:
                #with idx:
                    #i = [dict( id= p.fname, value= p.get(asp)) for p in parcheta ]
                    i = parcheta
                    i = [dict( (('n_'+k,v) for k,v in p.items() if k != 'id' and k[0]!='_' ),
                            **p)
                             for p in i]
                    print( i)
                    idx.update( i)#[dict( id= p.fname, value= p.get(asp)) for p in parcheta ])
        if optz.dump:
            for i in parcheta:
                print( i)
        tyrsi = optz.tyrsi

    if tyrsi:
        vypros = tyrsi
        if optz.index:
            k = optz.index
            if INFO:
                if k:
                    idx = getattr( ix.indexes, k)
                else:
                    idx = ix
                    assert k
                fieldname = 'value'
            else:
                fieldname = k
        else:
            fieldname = 'zaglavie'

        #or use FuzzyTermPlugin
        with idx:
            s = idx.searcher

            MAXDIST = 2     #edit distance
            MINDIST_PERC = 50     #or less than % of word
            MAXDIST_PERC = 80     #but not more than % of word
            PREFIX =  0     #minimum exact match at start of word

            #from whoosh import fields, index,

            from whoosh import query
            if 0:
                #qparser.FuzzyTermPlugin hooks direct to query.FuzzyTerm, so replacing that is too late
                qft__init__ = query.FuzzyTerm.__init__
                #def __init__(self, fieldname, text, boost=1.0, maxdist=1,
                #                prefixlength= PREFIX, constantscore=True):
                         #qft__init__( self, **dict( (k,v) for k,v in locals().items() if k != 'self' ))
                def __init__(self, *a,**ka):
                         qft__init__( self, prefixlength= ka.pop('prefixlength',PREFIX), *a,**ka)
                query.FuzzyTerm.__init__ = __init__

            def adist( size): return min(
                                max( MAXDIST, int( MINDIST_PERC * size/100.0 )),
                                int( MAXDIST_PERC * size/100.0 )
                                )

            if 0*'autofuzzy each word':
                #XXX beware: fires before anything else..
                from whoosh import qparser #  , analysis
                expr = qparser.FuzzyTermPlugin.expr
                expr = (
                        '((?P<eoword>\S)|' +
                        expr.pattern
                        +')'
                        + '(?=\\s|$)'   #XXX without this, original matches aa~bb
                        )
                qparser.FuzzyTermPlugin.expr = qparser.rcompile( expr, verbose= True)

                def eoword( m):
                    return max( 'eoword' in m.groupdict() and m.end('eoword') or 0, m.start(0) )
                def run():
                    for m in expr.finditer( 'one two~  tth~reeit'):
                        theword = m.string[ :eoword(m) ].rsplit()[-1]
                        print( m.groups(), m.span(0), m.span('maxdist'), theword)
            else:
                def eoword( m): return m.start(0)

            if 10*'control fuzzy params global and per-word':
                from whoosh import qparser #  , analysis
                #ocreate = qparser.FuzzyTermPlugin.create
                def create(self, parser, match):
                    theword = match.string[ :eoword( match) ].rsplit()[-1]
                    ltext = len( theword)

                    mdstr = match.group("maxdist")
                    maxdist = int(mdstr) if mdstr else adist( ltext)

                    pstr = match.group("prefix")
                    prefix = int(pstr) if pstr else PREFIX

                    print( 111111, maxdist, prefix, match.string, match.groups(), match.span(0), match.span('maxdist'), ltext, theword)
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

            # abc~3  maxdist-edits =3  default=1; 1replace=2edits
            # abc~3/2  maxdist-edits =3 , must-prefix = 3 default=0
            # "some phrase" all the words in that order
            # "some phrase"~3  max-word-distance between words = 3 , default 1 (consequtive)
            # 'some phrase' take literaly with spaces, commas,..

            qp = qparser.QueryParser( fieldname,    #can be [several]
            #p = qparser.MultifieldParser( ('value', 'ngram'),
                    schema= idx.ix.schema,
                    #group= qparser.OrGroup #.factory(0.9), # a b -> both a and b better than a and a
                )

            qp.remove_plugin_class( qparser.RangePlugin)
            qp.remove_plugin_class( qparser.BoostPlugin)
            qp.remove_plugin_class( qparser.EveryPlugin)    #??
            qp.remove_plugin_class( qparser.PhrasePlugin)
            qp.add_plugin( qparser.PlusMinusPlugin())
            qp.add_plugin( qparser.FuzzyTermPlugin())
            #from whoosh.query import FuzzyTerm
            #r = s.search( FuzzyTerm( 'value', vypros, maxdist=4, prefixlength=0 ), limit=None)
            #r = idx.find( vypros, limit=None, exact=False, maxdist=3)
            print( '??', vypros)
            #vypros = ' '.join( a+'~' for a in  vypros.split())
            print( '??', vypros)
            r = s.search( qp.parse( vypros ), limit=None)
            #print( r)
            print( ':::::::')
            for l in r:
                print( l.score, l.fields() ) #['value'])
            #print( ixx.get_alldata())

#   py t.py --tyrsi zaglavie=vor
#   py t.py --tyrsi zaglavie=bab
#   py t.py --tyrsi zaglavie=bab~1
#   py t.py --tyrsi zaglavie:rbab
#   py t.py --tyrsi 'zaglavie:rbab~1 avtor:ime'

# vim:ts=4:sw=4:expandtab
