#$Id: wiki-include-any.py,v 1.4 2008-06-18 12:58:57 sdobrev Exp $

#TRAC file-includer macro

try:
    from trac.wiki import wiki_to_html
#    from trac.WikiFormatter import WikiProcessor
    from trac import util
except ImportError,e:
    if __name__ == '__main__':  #fake it
        print e
        def wiki_to_html( text, env, req, db):
            return 'wiki_to_html:' + repr(text)
        class util:
            class TracError( Exception): pass
    else:
        raise

import os

ARG_DELIMITER = ','
WIKI_PREFIX   = 'wiki'
SRC_PREFIX    = 'source'
SRCWIKI_PREFIX= 'source_as_wiki'

__doc__ = help = '''\
The "includer" macro requires an url as argument. Possible url/types:

  %(WIKI_PREFIX)s:PageName(,(value|key=value))*::
    Load page from the wiki and try to substitute positional/keyword-argument
    references in it if any, so the page can be used as a template. Unsatisafied
    references (and everything else) is left as-is. Uses wiki-Formating
          * positional args are referenced as {{number}}
          * keyword args are referenced as {{keyword}}
          *  (keyword can be a number too - for pages that already have numbers)
    Examples:
          * %(WIKI_PREFIX)s:FlowerRose                                   ---plain
          * %(WIKI_PREFIX)s:FlowerDescr,Rose,red,strong                  ---template/pure-positional-args
          * %(WIKI_PREFIX)s:FlowerDescr,2=red,3=strong,1=Rose            ---template/keyword-args-as-positional
          * %(WIKI_PREFIX)s:FlowerDescr,name=Rose,color=red,smell=strong ---template/pure-keyword-args
          * %(WIKI_PREFIX)s:FlowerDescr,Rose,color=red,smell=strong      ---template/mixed
          * %(WIKI_PREFIX)s:FlowerDescr,2=red,1=Rose,smell=strong        ---template/additional-keyword-arg to old positionals

  %(SRC_PREFIX)s:/file/path/in/repository::
    load file from the attached svn repository - dont forget trunk/ or branch/whatever prefix

  %(SRCWIKI_PREFIX)s:/file/path/in/repository::
    same as above but shown as wiki page

  /file/in/server/filesystem::
    anything starting with / is interpreted as absolute path - urllib.openurl()

  url: e.g. http://my.server/whatever/file::
    as of urllib.openurl()

modulepath: %(__file__)s
''' % locals()

def wiki( req, argument_text, env):
    args = argument_text.split( ARG_DELIMITER )
    name = args[0].replace( "'", "''")
    if not name:
        raise util.TracError( help )

    from trac.wiki import model
    page = model.WikiPage( env, name)
    header = wiki_to_html( '[wiki:%(name)s] / %(argument_text)s:\n' % locals(), env,req)

    text = ''
    if page.exists:
        text = page.text
        for i in range(1,len(args)):
            arg = args[i]
            try:    #keyword-args
                key,value = arg.split('=')
            except ValueError:
                #positional args
                format = '{{%(i)d}}'
                value = arg
            else:
                format = '{{%(key)s}}'
            text = text.replace( format % locals(), value )
        text = wiki_to_html( text, env, req)
    return text, header

import os.path

def source( req, argument_text, env, aswiki =False):
    from trac.versioncontrol.web_ui.util import get_existing_node, get_path_rev_line
        ## XXX above .util is shaded by trac.util?

    path,rev,line = get_path_rev_line( argument_text)
    from trac.mimeview import Mimeview, get_mimetype, content_to_unicode

    repos = env.get_repository() # req.authname)
    node = get_existing_node( env, repos, path, rev)
    content = node.get_content().read()
    if aswiki:
        mimetype = 'text/x-trac-wiki'
        r = wiki_to_html( content_to_unicode( env, content, mimetype), env=env, req=req)
    else:
        mimetype = get_mimetype( os.path.basename( path) ) or 'text/plain '
        mimeview = Mimeview( env)
        #charset = mimeview.get_charset( content, mimetype) #node.content_type?
        #content = util.to_utf8( content, charset )
        r = mimeview.render( req, mimetype, content)
    return r, None

#<META Http-Equiv="Content-Type" Content="text/html; charset=windows-1251">

_error_url = 'cannot open url "%(url)s" - is it a valid link?'
import re
_meta_charset = '''< meta
http-equiv = "content-type"
content = "\S+ ; charset = (\S+)" >'''.replace(' ','\s*').replace('\n','\s+')
#print _meta_charset
_re_meta_charset = re.compile( _meta_charset, re.IGNORECASE )

def url( req, argument_text, env):
    'can be also done as html-inline-frame or html-object - instead of direct-insert-inline'
    import urllib
    url = argument_text
    try:
        f = urllib.urlopen( url)
    except:
        raise util.TracError( _error_url % locals() )

    text = f.read()
    m = _re_meta_charset.search( text)
    if m:
        charset = m.group(1)
        text = util.to_utf8( text, charset.lower() )

    if 0:
        path,suffix = os.path.splitext( argument_text)
        suffix = suffix[1:]     #skip . from .xxx
        try:
            Format = WikiProcessor( env, suffix)
            html = Format.process( req, text)
            return html, None
        except:
            pass
    return util.Markup( text), None   #raw?

def sourceaswiki( *a): return source( aswiki=True, *a)

_processors = {
    WIKI_PREFIX: wiki,
    SRC_PREFIX:  source,
    SRCWIKI_PREFIX:  sourceaswiki,
}

def execute( req, argument_text, env):
    # ??? Currently req is set only when the macro is called From a wiki page

    if not argument_text:
        raise util.TracError( help)
    try:
        if req: req.href = env.href     #XXX HACK to avoid wiki_to_html error

        for pfx,func in _processors.iteritems():
            pfx+=':'
            if argument_text.startswith( pfx):
                r = func( req, argument_text[ len(pfx):], env)
                break
        else:
            r = url( req, argument_text, env)
        r,header = r

        if not header:
            header = wiki_to_html( '[%(argument_text)s]\n' % locals(), env=env, req=req)
    except Exception, e:
        header = str(type(e))+':'+repr(e)
        import traceback
        r = '\n<hr>\n'+traceback.format_exc().replace('\n','<BR>\n')

    return header + r

if __name__ == '__main__':
    import sys
    class Allfake:
        def cursor(me): return me
        def execute(me,txt): pass
        def fetchone(me): return ['aaaa b c d e 1:{{1}} boza:{{boza}} 3:{{3}}']

        class href:
            base = '/base-h/ref/'
        def get_db_cnx(me): return me
    args = sys.argv[1:]
    if not args: args = [
	        'http://www.dir.bg',
	        '/tmp/WikiFile.py',
	        'wiki:mywiki,a1,a2',
	        'wiki:mywiki,a1,a2,a3,boza=bzu',
	        'wiki:mywiki,3=a3,1=a1,boza=bzu,2=a2,',
	        'source:url/srcfile.exam',
            ]

    env = Allfake()
    for arg in args:
        print '------ execute', arg
        print execute( None, arg, env=env )

# vim:ts=4:sw=4:expandtab
