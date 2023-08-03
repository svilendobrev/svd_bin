#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function #,unicode_literals
'''
https://docs.gitlab.com/ee/api/graphql/getting_started.html
####
manual: you get the pages
 https://gitlab.ecollect.org/-/graphql-explorer
 use gql_query below, previous_page_endCursor must have double-quotes "" unless is null
 save result pages into files
 pass them as args
auto: it get the pages by itself
 make personal-access-token in gitlab > usermenu > edit-profile
 save+pass it as arg -t=thetoken
'''

gql_url_POST = 'https://gitlab.ecollect.org/api/graphql'

#see https://docs.gitlab.com/ee/api/graphql/reference/#project
#previous_page_endCursor = null for first or "whatever-endCursor-is" in quotes for other pages
gql_query = '''
query {
  projects( after:%(previous_page_endCursor)s) {
    pageInfo { endCursor startCursor }
    nodes {
        group { fullName }
        fullPath
        lastActivityAt
        createdAt
        visibility
        archived
        mergeRequests { count }
        statistics { commitCount }
        }
  } }
'''

import json
#import pprint

projects = {}
def add_page( pagedict):
    #print(f)
    #pp = json.load( open( f)) #open('gitlab.projects.json'))
    pp = pagedict
    qq = sorted( pp['data']['projects']['nodes'], key= lambda p: p['fullPath'] )
    #pprint.pprint( qq)
    news= dict( (p['fullPath'],dict(
            updated= p['lastActivityAt'],
            created= p['createdAt'],
            merges = int( p['mergeRequests']['count']),
            commits= int( p['statistics']['commitCount']),
            visible= p['visibility'],
            archived= p['archived'],
            )) for p in qq)
    overlaps = set(news) & set(projects)
    assert not overlaps, overlaps
    projects.update( news)

def show_projects():
    #pprint.pprint( projects)
    print('{')
    for k,v in sorted( projects.items()): print( f'{k!r:50}: {v!r},' )
    print('}')

import argparse
ap = argparse.ArgumentParser( description= '''\
extract info about projects in gitlab.
if given personal-access-token via --token , obtains all data from gitlab/graphql --url ;
and/or reads input files as manually saved json-pages (see source for procedure)
''')
ap.add_argument( '--url', default= gql_url_POST, help= 'gitlab-api.graphql url, default= %(default)s')
ap.add_argument( '--token', help= 'personal-access-token , from gitlab > usermenu > edit-profile')
ap.add_argument( 'inputs', nargs='*', help= 'json-pages, manually saved')

optz = ap.parse_args()

token = optz.token
for fi in optz.inputs:
    add_page( json.load( open( fi)))

##### auto
if token:
    try: from . import httprr
    except ImportError: import httprr
    req_resp = httprr.req_resp
    jsonresp = httprr.json_resp
    #import base64

    def gitlab_grapfql_query( q ):
        resp = req_resp( optz.url, dict( query= q),
                    **({} if not token else dict(
                        #headers= dict( Authorization= 'Basic '+ base64.b64encode( (usr+':'+psw).encode( 'utf8') ).decode('ascii'))
                        headers= dict( Authorization= f'Bearer {token}' ),
                        )),
                    json= True, debug= 0 )   #POST
        js = jsonresp( resp)['json']
        return js

    def getprev_end( page):
        if not page: return 'null'  #first page
        endCursor = page['data']['projects']['pageInfo']['endCursor']
        if not endCursor: return    #last page
        return f'"{endCursor}"'

    def pager( ):
        prevpage_end = getprev_end( None)
        while 1:
            page = gitlab_grapfql_query( gql_query % dict( previous_page_endCursor= prevpage_end))
            if not page: break      #does not happen; instead gets empty thing: {data:{projects:{pageInfo:{endCursor:null,startCursor:null},nodes:[]}}}
            prevpage_end = getprev_end( page)
            if not prevpage_end: break
            yield page

    for page in pager():
        add_page( page)

show_projects()

# vim:ts=4:sw=4:expandtab
