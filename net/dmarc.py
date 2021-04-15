#!/usr/bin/env python

import xml.etree.ElementTree as ET
import time
import zipfile

def find( e, t, as_text =True):
    r =list(e.iter( t))[0]
    if as_text: r = r.text
    return r

def parser( fname):
    try:
        z = zipfile.ZipFile( fname)
        assert len( z.namelist()) == 1
        fname = z.open( z.namelist()[0])
    except: pass

    tree = ET.parse( fname)
    root = tree.getroot()
    # Metadata
    print( getattr( fname, 'name', fname), "#################")
    daterange = find( root, 'date_range', False)
    beginDate = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int( find( daterange, 'begin'))))
    endDate   = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int( find( daterange, 'end'))))
    print( 'by:', find( root, 'org_name'), find( root, 'report_id'), '\t period:', beginDate, '-', endDate)

    # IP Data
    for record in root.findall('record'):
        for row in record.findall('row'):
            print( ' ', str(dict(
                ip=     find( row, 'source_ip'),
                count=  find( row, 'count'),
                )).replace("'",''))
            for policy_evaluated in row.findall('policy_evaluated'):
                print( '   ', str(dict(
                    what= find( policy_evaluated, 'disposition'),
                    dkim= find( policy_evaluated, 'dkim'),
                    spf=  find( policy_evaluated, 'spf'),
                    )).replace("'",''))

if __name__ == '__main__':
    import sys
    for a in sys.argv[1:]:
        parser( a)

# vim:ts=4:sw=4:expandtab
