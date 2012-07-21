# -*- coding: utf-8 -*-
from opisvane import prn, DictAttr, dictOrder, str2list

import yaml
from util.yamls import yaml_anydict, yaml_extra

class Dumper( yaml_extra.Dumper_AlignMapValues,
              yaml_extra.Dumper_PreferBlock_for_Multiline,
              yaml_extra.Dumper_AllowExtraWidth_for_Singleline,
            yaml.Dumper ):
    extra_width = 15

    def represent_list( self, data):
        #if len( data) == 0: return
        if len( data) == 1:
            return self.represent_data( tuple(data)[0] )
        return super( Dumper, self).represent_list( data)


class Loader( yaml_anydict.Loader_map_as_anydict, yaml.Loader):
    anydict = dictOrder

def dump( d):
    return yaml.dump( d, allow_unicode= True, default_flow_style= False, Dumper= Dumper)
        #width=90,

#yaml_anydict.dump_anydict_as_map_inheriting( dictOrder)
yaml_anydict.dump_anydict_as_map_inheriting( dict)
yaml_anydict.dump_seq_as_list( tuple, Base=Dumper)
yaml_anydict.dump_seq_as_list( set,   Base=Dumper)
yaml_anydict.dump_seq_as_list( list,  Base=Dumper)

Loader.load_map_as_anydict()
yaml_anydict.load_list_as_tuple()


class opis_io:
    PFX_GRUPA_DOP = '+='
    @classmethod
    def zapis( klas, az, d =None, naistina =False ):
        d = d or az.danni()

        dd = dictOrder()
        def slozhi( k):
            v = getattr( d, k)
            if isinstance( v, str) and v.isdigit(): v = int(v)
            if v or v==0: dd[ az.stoinosti[k] ] = v

        slozhi( 'ime')
        slozhi( 'imena')

        for (obhvat, e_simvol), stoinosti in sorted( d.etiketi.items(), key= lambda kv: (kv[0][0],not kv[0][1]) ):
            if not stoinosti: continue

            if obhvat:
                r = dd.setdefault( az.stoinosti[ obhvat], dictOrder() )
            else: r = dd
            if e_simvol:
                r[ az.stoinosti.simvoli ] = ' '.join( stoinosti)
            else:
                for k,vv in stoinosti:
                    if not isinstance( vv, (tuple, list)): vv = [vv]
                    #vv = [ v.strip() if isinstance( v, str) else v for v in vv ]
                    vv = [ int(v) if isinstance( v, str) and v.strip().isdigit() else v
                            for v in vv ]
                    if len(vv)==1: vv = vv[0]
                    r[ k] = vv

        kv4prev = [ az.stoinosti.ime, az.stoinosti.simvoli ] + [ az.stoinosti.get( k,k) for k in az.Prevod._vytr_svoistva]
        def prev( p):
            r = [ (az.stoinosti.ime, p.ime) ]
            if p.etiketi:
                r += [ ( az.stoinosti.simvoli, ' '.join( p.etiketi)) ]
            r += [ #(az.stoinosti[k],v)
                    (k,v)
                    for k,v in sorted( p.items())
                    if v and k not in kv4prev ]
            return ( p.fname, len(r) > 1 and dictOrder( r) or p.ime)
        def prevodi2zapis( pr):
            return dictOrder( prev(p) for p in pr)

        if d.prevodi:
            dd[ az.stoinosti.prevodi] = prevodi2zapis( d.prevodi)
        if d.grupi:
            gg = [ dict( (k,v) for k,v in {
                     az.stoinosti.grupa: g.kyso,
                     az.stoinosti.ime:   g.dop and klas.PFX_GRUPA_DOP + g.dop or g.ime != g.kyso and g.ime or '',
                     az.stoinosti.prevodi: prevodi2zapis( g.elementi)
                    }.items() if v )
                    for g in d.grupi ]
            dd[ az.stoinosti.grupi] = gg

        r = dump( dd)
        VIMtail = '# v' + 'im:ts=4:sw=4:expandtab:ft=yaml' #separated!
        if d.komentari:
            r += '\n'+'\n'.join( d.komentari)
            if d.komentari[-1].lstrip('# ').startswith('vim:'): VIMtail= None
        if VIMtail: r += '\n'+VIMtail
        return az._zapis( r, az.redove, naistina= naistina, ext= '.yaml')

    @classmethod
    def otgatni( klas, az, redove):
        for r in redove:
            r= r.strip()
            if not r or r[0]=='#': continue
            for kk in az.stoinosti_imena[ az.stoinosti.ime]:
                if r.startswith( kk+':'): return True

    @classmethod
    def procheti( klas, az, redove):
        az.redove = redove
        az.komentari = [ r for r in redove if r.startswith('#') ]
        d = yaml.load( '\n'.join( redove), Loader= Loader)
        assert isinstance( d, dictOrder)

        e = {}
        for k,v in d.items():
            az._slaga_etiket( k,v, zamesti= True, rechnik= e)
        #?? e = make_dict_trans()( _prevodach= az.stoinosti)

        az.slaga_ime(    e.pop( az.stoinosti.ime).strip() )
        az.imena.update( e.pop( az.stoinosti.imena, () ))

        ss = str2list( e.pop( az.stoinosti.sydyrzhanie, () ))
        if ss: az.etiketi.sydyrzhanie = ss

        prevodi = e.pop( az.stoinosti.prevodi, {})
        grupi   = e.pop( az.stoinosti.grupi, ())

        #общи, само папка, само елементи
        papka   = e.pop( az.stoinosti.papka, {})
        element = e.pop( az.stoinosti.element, {})
        def slaga( vhodni, rechnik):
            simvoli = vhodni.pop( az.stoinosti.simvoli, '').strip().split()
            for k in simvoli:
                az._slaga_etiket( k, True, rechnik)
            for k,v in vhodni.items():   #останалите
                az._slaga_etiket( k,v, rechnik, zamesti= True)
        slaga( e, az.etiketi)
        slaga( papka, az.etiketi_papka)
        slaga( element, az.etiketi_element)

        klas._prevodi( az, prevodi)

        for gg in grupi:
            g = {}
            for k,v in gg.items():
                az._slaga_etiket( k,v, zamesti= True, rechnik= g)

            kyso = g.get( az.stoinosti.grupa )
            dylgo = g.get( az.stoinosti.ime, '')
            if dylgo.startswith( klas.PFX_GRUPA_DOP):
                dop = dylgo[ len( klas.PFX_GRUPA_DOP):]
                dylgo = ''
            else: dop = ''

            prevodi = g[ az.stoinosti.prevodi]
            igrupa = az.nova_grupa( dylgo= dylgo, kyso= kyso, dop= dop )
            klas._prevodi( az, prevodi, igrupa)

    @classmethod
    def _prevodi( klas, az, prevodi, grupa =None):
        if isinstance( prevodi, dict):
            for f,vo in prevodi.items():
                vv = None
                if isinstance( vo, str): vv = dict( ime= vo)
                elif isinstance( vo, dict):
                    if len(vo)==1:
                        ime,uch = list(vo.items())[0]
                        assert isinstance( ime, str), ime
                        assert isinstance( uch, (str, tuple, list, dict)), vo
                        e_ime_uchastnici = ime not in az.rstoinosti
                        if e_ime_uchastnici:
                            vv = dict( ime=ime, uchastnici= uch )
                    if not vv:
                        for k,v in vo.items():
                            if v is None: continue
                            assert isinstance( k, str), vo
                            assert isinstance( v, (int, str, tuple, list, dict)), vo
                        vv = dict( (az.rstoinosti.get(k,k),v) for k,v in vo.items())
                else:
                    v,o = vo
                    vv = dict( ime=v, original=o)
                az.nov_prevod( fname= f, grupa= grupa, roditel= az.fname, **vv)
        else: #list
            for kvo in prevodi:
                if isinstance( kvo, (tuple,list)):
                    vv = dict( fname= kvo[0], ime=kvo[1] )
                    if len(kvo)>2: vv.update( original= kvo[2])
                    assert len(kvo)<=3
                else: #dict
                    vv = dict( (az.rstoinosti.get(k,k),v) for k,v in kvo.items())
                az.nov_prevod( grupa= grupa, roditel= az.fname, **vv)
        ''' варианти:
            fname: ime
            fname: [ ime, original ]
            fname:
                ime: uchastnici
            fname:  #най-пълно1
              _ime: ime
              _opis: opis
              _uchastnici: ...
            - #най-пълно2
              _fname: fname
              _ime: ime
              _opis: ...
            - [ fname, ime ]
            - [ fname, ime, original ]
        '''
# vim:ts=4:sw=4:expandtab
