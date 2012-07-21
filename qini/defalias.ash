al py python
al python python2.5

al d 'ls -1lF'
al d. 'ls -alF'

al _d2  "perl -e 'while(<>)"'{if (/^d/||/\/$/) {print} else {push @a,$_}}'" print @a'"
d2() 	{ d --color "$@" | _d2; } #force coloring

al dlinkbroken 'find . -type l -exec ls -alF --color {} \; | grep "31;1" '
al df 'LANG=C df -h'

al up   "cd .."
al md   mkdir
al rd   rmdir
nd() 	{ md -p "$1" ; cd "$1"; } 
al mv   'mv -i'

al g    'grep -E'

al zx   unzip
al zv   "zx -v"
al xz   zx

 #-i: smart case-nonsensitive search; -S: don't wrap long lines; -X: disable init screen save/restore
senv    LESS '-i -S -X'
al l    less

al t    cat
al tm   date
al qt   date
al zap  "rm -rf"
#al e    "vim -n"    #no swap - memonly
#al vimdiffexactws    "e -d --cmd 'let diff_ws_exact=1'"
al m    make
al em   "e [Mm]akefile"
al renl "rename.pl y/A-Z/a-z/"  #this works only if  LC_COLLATE=C !!
al renu "rename.pl y/a-z/A-Z/"
al top  "top -d 1"
al sort 'LC_ALL=C sort'
al wh   which

al eng  'env | g'
al seg  'set | g'
al alg  'alias | g'


# tar from stdin: tar vt  or  or tar vtf -
al tv   "tar vtf"
al tx   "tar vxf"
#if tar --version | grep GNU >/dev/null ; then
 al tgzv 'tar tzvf'
 al tgzx 'tar xzvf'
 al tbzv 'tar tjvf'
 al tbzx 'tar xjvf'
 al tzv  'tar tZvf'
 al tzx  'tar xZvf'
#else
# al tgzv 'gzip -dc \!:1 | tv -'
# al tgzx 'gzip -dc \!:1 | tx -'
# al tbzv 'bzip2 -dc \!:1 | tv -'
# al tbzx 'bzip2 -dc \!:1 | tx -'
# al tzv  'uncompress -dc \!:1 | tv -'
# al tzx  'uncompress -dc \!:1 | tx -'
#fi

al psu  'ps -u $USER'   # BSD style; override if other layout
test 0 == `id -u` && al psu  'ps ax'   # BSD style; override if other layout
al psfu 'psu -f'
al pme  'psfu ;jobs -l'     # my processes and jobs
 # my processes, sorted by starttime+PID; or try PPID,PID (3 then 2)
#al mi   'psfu |sort -k 5,5 -k 2;jobs -l'
al mi   'psfu ;jobs -l'
al k9   "kill -9"
killalll() 	{ Z=`psfu | g "$1" | grep -v grep | cut -c10-15` && test -n "$Z" && k9 $Z; } 

al lo   'cd ${_INIs}; make; so defalias$_EXT; cd -'

al fc   "diff -btw"

ffl() 	{ find . -${II}name "$@"; } 
 #-follow sym-links
fff() 	{ find . -follow -${II}name "$@"; } 
ff() 	{ fff "$@" -exec ls -dF '{}' ';'; } 
al ffi   "II=i ff"
al fffi  "II=i fff"
al ffli  "II=i ffl"
# !!! for any other * finds use fff.sh !

 # /dev/null added to force grep to prefix each line with filename even if one file only
ggg() 	{ grep -Ens "$@" /dev/null; } 

##grep whatever whereever including all source-type files (c,c++,asm); make yours
senv _SRC  "\*.[cChylg] \*.[ch]pp \*.[ch]xx \*.cc \*.CC \*.asm \*.p[yl] \*.java \*.js \*.xsl"

 #recursive     from current dir grep in source files ONLY
 ###stupid grep cannot ignore whole-dirs - only files!
grs() 	{ ggg -r --exclude=\*.svn-\* "$@" . `echo $_SRC | sed 's/\\\\/--include=/g'` ; } 
al gr  grs
grm() 	{ ggg -r --exclude=\*.svn-\* "$@" . --include=[mM]akef\* --include=*.mak ; } 
grh() 	{ ggg -r --exclude=\*.svn-\* "$@" . --include=\*.htm\*   --include=\*.css ; } 

#see fff.sh for quote troubles
senv FCSRC 'CVS* *.pyc *.so *.[oa] *.exe *.proj .snprj *.dep *.req _obj *.gen _*.fsm *.ok *.xx *.result *.tmp _allin1* .#* *.jar *.bin dependencies objects *.class .cvsignore .svn tags .bzr .hg .hgtags'
fcsrc() 	{ set -f; fc -r -I "\$Id.*\$" -I "\$Rev.*\$" `for a in $FCSRC; do echo -x "$a"; done ` "$@"; set +f; } 

calc() 	{ echo print "$@" | python ; } 

al rmpyc 'find . -follow -name \*.pyc -exec rm {} \;'
al rmpycl 'find . -name \*.pyc -exec rm {} \;'
