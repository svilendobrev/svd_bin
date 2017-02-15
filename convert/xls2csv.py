#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function #,unicode_literals

USE_XLRD=0
if USE_XLRD:
    import xlrd
    #this puts ints as floats :/ and formatting_info is not there yet
else:
    import openpyxl
    #if 123 is formatted under 0000 -> manual reformat-to-text

ALLSHEETS = object()
def read( fname, sheets =[], as_sheet =False):
    if USE_XLRD:
        wb = xlrd.open_workbook( filename= fname, formatting_info= True )   # no formatting_info yet :(
        wsnames = wb.sheet_names()
    else:
        wb = openpyxl.load_workbook( filename= fname,
                    read_only= True,
                    guess_types=False,
                    )
        wsnames = wb.get_sheet_names()

    if not sheets:
        if len(wsnames) >1:
            print( 'cannot choose, more than one available sheets:')
            for ws in wsnames: print( ' ', repr(ws))
            raise SystemExit(1)

        wsnames = [ wsnames[0] ]
    elif sheets is not ALLSHEETS:
        wsnames = sheets

    for sname in wsnames:
        def value( cell): return cell.value
        if USE_XLRD:
            ws = wb.sheet_by_name( sname)
            rows = ws.get_rows()
        else:
            ws = wb[ sname ]
            rows = ws.rows

            def value( cell):
                if cell.value is not None:
                    if cell.number_format and cell.number_format.startswith('0'):
                        return str(cell.value).zfill( len( cell.number_format ))
                return cell.value

        if not as_sheet:
            ws = [ [ value( cell) for cell in row]
                    for row in rows ]
        yield sname.strip(), ws


def strip( array):
    #right
    maxw = 0
    for row in array:
        i=0
        for i,cell in enumerate( row[::-1]):
            if cell is not None: break
        w = len(row)-i
        maxw = max( maxw, w)
    for row in array:
        row[ maxw:] = []

    #bottom
    i=0
    for i,row in enumerate( array[::-1]):
        if any( cell is not None for cell in row): break
    maxh = len(array)-i
    array[ maxh:] = []

    print( 'w', maxw, 'h', maxh)
    return array

import csv
def write( fname, array):
    #with open( fname, 'wb') as f: nonono
    try:
        f = open( fname, 'x', newline='')
    except FileExistsError:
        print( '! file exists', fname)
        return
    print( '>', fname)
    with f: #open( fname, 'w', newline='') as f:
        c = csv.writer(f)
        for row in array:
            c.writerow( row )

if __name__ == '__main__':
    from svd_util import optz, osextra
    optz.help( '''
extract excel sheet(s) into .csv
args-in-any-order: file.xlsx [sheetname] [sheetname] ..
 unless --allsheets, no sheet-names means first if only one, else shows all sheet-names and stops
 examples:
    ... path/to/somename.xls --all --dir --path .   -->> dumps all sheets as ./somename/sheetname*.csv

'''.strip())
    optz.str( 'csv',        help= 'name of output file.csv ; used as prefix if allsheets; defaults to path+name of file.xlsx + .sheetname-if-specified')
    optz.str( 'path',       help= 'output path, default is whereever .xls is')
    optz.bool( 'allsheets', help= 'save all sheets, named csvname.sheetname.csv')
    optz.bool( 'dir_from_name',  help= 'create outname as folder, i.e. csvname/sheetname.csv')
    optz.bool( 'nostrip',   help= 'do not strip empty columns/rows at right/bottom')
    oparser = optz.oparser
    optz,argz = optz.get()
    fcsv = optz.csv
    sheets = []
    fxls = None
    for a in argz:
        if a.endswith( '.xls') or a.endswith( '.xlsx'):
            fxls = a
        else: sheets.append( a )

    if not fxls:
        oparser.error( 'needs .xls or .xlsx file')
    if optz.allsheets:
        if sheets: oparser.error( 'needs either --allsheets or sheetnames, not both')
        if fcsv:  print( 'auto-appending sheetnames to .csv name')
        sheets = ALLSHEETS

    from os.path import join,basename
    if not fcsv:
        fcsv = osextra.withoutext( fxls, '.xlsx', '.xls')
    else:
        fcsv = osextra.withoutext( fcsv, '.csv')
    if optz.path:
        osextra.makedirs( optz.path)
        fcsv = join( optz.path, basename( fcsv))
    if optz.dir_from_name:
        osextra.makedirs( fcsv)
    for sheetname, data in read( fxls, sheets):
        if not optz.nostrip: data = strip( data)
        afcsv = fcsv
        if sheets:
            afcsv += ('/' if optz.dir_from_name else '.') + sheetname
        write( afcsv + '.csv', data)

# vim:ts=4:sw=4:expandtab
