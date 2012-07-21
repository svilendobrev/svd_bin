#!/usr/bin/env python
# -*- coding: utf-8 -*-
#$Id$
import sys
from spisyk_nadpisi import parse
fname_spisyk = sys.argv.pop(1)
spisyk = parse( fname_spisyk)

title = 'Албум на випуск 2008 от детска градина "1-ви юни"'
print '''<html>
<title>
 %(title)s
</title>
<body>
<center>
 <h2> %(title)s <br>
 <hr>
</center>
''' % locals()

for l in sys.stdin:
    l = l.strip()
    if not l or l.startswith('#'): continue
    name = l
    if name=='drugi':
        text = 'други снимки, които не са влезли в албума'
    else:
        img_nomer = name.split('_')[-1].split('.')[0]
        oname,priakor,ime = spisyk.get( 'img_'+img_nomer, (name,name,name) )
        text = priakor + ' - ' + ime
    print '''
<table ><tr>
<td> &nbsp; &nbsp; &nbsp;
<td>
<img src="%(name)s">
<td> &nbsp; &nbsp; &nbsp;
<td>
 %(text)s: <br>
 <a href="%(name)s"> 1:4 малка    <br>
 <a href="2/%(name)s"> 1:2 средна <br>
 <a href="1/%(name)s"> 1:1 голяма <br>
</table>
<hr>
''' % locals()

print '</html>'
# vim:ts=4:sw=4:expandtab
