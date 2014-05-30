#!/usr/bin/env python2

# Written by Henry 'Pi' James and Loring Holden
# modified for multitracker display by John Hoffman
# see LICENSE.txt for license information
#use: python btshowmetainfo.py [file.torrent]
#XXX refaktored

from sys import argv
from os.path import *
from sha import *

# from BitTornado.bencode import *
from bencode import *

VERSION = '20030621'

if len(argv) == 1:
    print argv[0], 'torrent-files ...' 
    print
    exit(2) # common exit code for syntax error

for metainfo_name in argv[1:]:
    metainfo_file = open(metainfo_name, 'rb')
    metainfo = bdecode(metainfo_file.read())
    #print metainfo
    info = metainfo['info']
    info_hash = sha(bencode(info))

    print 'metafile:\t', basename(metainfo_name)
    piece_length = info['piece length']
    if info.has_key('length'):
        # let's assume we just have a fil3
        print 'file name\t', info['name']
        file_length = info['length']
        name ='file size      '
    else:
        # let's assume we have a directory structure
        print 'directory name: %s' % info['name']
        print 'files:'
        file_length = 0;
        for file in info['files']:
            path = '/'.join( file['path'])
            print '   %s (%d)' % (path, file['length'])
            file_length += file['length']
            name ='archive size   '
    piece_number, last_piece_length = divmod(file_length, piece_length)
    print '%s %i (%i * %i + %i)' % (name,file_length, piece_number, piece_length, last_piece_length)

    print 'info hash\t', info_hash.hexdigest()
    print 'announce url\t', metainfo['announce']
    if metainfo.has_key('announce-list'):
        print 'announce-list   '+ '|'.join( 
            ','.join( tier)
            for tier in metainfo['announce-list']
            )

    if metainfo.has_key('httpseeds'):
        print 'http seeds\t', ''.join( 
            '|'.join( seed)
            for seed in metainfo['httpseeds']
            )
    if metainfo.has_key('comment'):
        print 'comment: \t', metainfo['comment']

        print '---'

# vim:ts=4:sw=4:expandtab
