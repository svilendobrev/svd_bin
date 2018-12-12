#!/bin/bash
# vcs.sh, 2002-2012 s.dobrev

#common interface to cvs svn bzr hg git:
# - wrapper for frequently used commands (vcs.sh)
# - colorizer, in the spirit of colorcvs/colorsvn family, but simpler/smaller (colorvcs.py)
# the wrapper works fine without the colorizer (but looks for it via `which` ).
#
# The vcs-guessing is by looking for ./CVS ./.svn in ./, or .bzr .hg .git in ./ and 9 levels up
# any extra args are passed untouched
# tweaks:
#  export svn_d_args=... (e.g. for svn diff) and alike to (constantly) locally tweak commands:
#         # e.g. export svn_d_args='--diff-cmd diff -x -btw -x -U5'
#  export NOCOLOR=1    # will avoid invoking colorizer from vcs
#
# my preferred usage is having both in path, and
# sym-linking vcs to be called 'v' and also 'u' :
#  $ u ... does update, same as v u
#  $ v u ... does update
#  $ v s ... does status
#  $ v i -m fixx ... does commit AND push
#  $ v il -m fixx ... does commit local (same as above is no such notion)
#  $ v ii ... resolve conflict
#  $ v d ... does diff
#  $ v dd ... does diff ignoring whitespace
#  $ v r ... does remove
#  $ v a ... does add
#  $ v l ... does log
#  $ v n ... does info, e.g. repository urls, revisions, etc
#  $ v v ... does revert -- this one asks for confirmation - happened to kill a file
#  $ v p ... does push
#  $ v m ... does merge
#
# there are also other naming schemes below (e.g. can be linked as v-status or vvs) but of no use..

#E=echo

KNOWN='cvs svn bzr hg git'
what=

## these in each level/dir
if test -f CVS/Root       ; then  what=cvs
elif test -f .svn/entries ; then  what=svn
else
    ## these once in root of repository
    d=./
    for ((a=19;a--;)) do
        if test -d $d.bzr; then  what=bzr; break;
        elif test -d $d.hg; then  what=hg; break;
        elif test -d $d.git; then  what=git; break;
        elif test -f $d.svn/entries ; then  what=svn
        fi
        d=../$d
    done

    if test -z "$what"; then
        echo "  !unknown directory non-($KNOWN)"; exit 1
    fi
fi

#echo $0
cmd=
b=`basename $0`
case $b in
    [raulid]|ii|dd) cmd=$b ;;
    v|vcs.sh) cmd=$1; shift ;;
#    v-update|vvu) cmd=u ;;
#    v-commit|vvi) cmd=i ;;
#    v-diff|vvd)   cmd=d ;;
#    v-log|vvl)    cmd=l ;;
#    v-add|vva)    cmd=a ;;
#    v-remove|vva) cmd=r ;;
#    v-status|vvs) cmd=s ;;
#    v-revert|vvv) cmd=revert ;;
    *) echo "   unknown basename-command for $KNOWN: $b"; exit 1 ;;
esac

#################### passing spaces is HARD XXX
cvs_u='up -Pd'
cvs_i='ci'
cvs_il='ci'
cvs_ii='ci'
cvs_d='diff -bw'
cvs_dd=$cvs_d
cvs_l='log'
cvs_a='add'
cvs_r='rm -f'
cvs_s='stat'
cvs_n='stat'
cvs_v='up -C'
#no merge
#no push

svn_u='update'
svn_i='ci'
svn_il='ci'
svn_ii='resolved'    #after conflct, before commit + needs another commit
svn_d='diff'
svn_dd='diff --diff-cmd diff -x -btwU3'
svn_dprev='diff -r PREV'
svn_l='log'
svn_a='add'
svn_r='rm'
svn_s='stat'
svn_n='info'
svn_v='revert'
svn_m='merge'
#no push

svn_s_pipe="| grep -vE '(Performing status on external item at|^$)'"
svn_u_pipe="| grep -viE '(external |^$)'"

bzr_u='update'
bzr_i='commit'
bzr_il='commit --local'
bzr_ii='resolve'    #after conflct, before commit + needs another commit
bzr_d='diff'
bzr_dd='diff --diff-options=-btwU3'
bzr_dprev='diff -r -2'
bzr_l='log'
bzr_a='add'
bzr_r='rm'
#bzr_s='status'
#bzr_s='ecmd -- status'  #externals???
bzr_s="`test -f $d/.bzrmeta/externals && echo 'ecmd --'` status"  #externals???
bzr_ss="status"
bzr_n='info'
bzr_n_pipe='; bzr revno'
bzr_v='revert'
bzr_m='merge'
#bzr_p='push'    #not needed, plain commit does it
bzr_io="missing ; bzr $bzr_s"    #missing needs pull-branch remembered: bzr pull the-url
bzr_oi="$bzr_io"
bzr_hs='shelve'
bzr_hu='unshelve'

hg_u='pull -u'
hg_u_pipe='| grep -v searching.for.changes || (echo "! unresolveds !" && false)'  #false: propagate the error (as echo->success) ; || && =same priroty ; grep needs -o pipefail
hg_uu='update'
hg_i='commit'
hg_p='push'
#hg_i_pipe='&& hg push'
hg_ii='resolve -m'    #??? after conflct, before commit + needs another commit
hg_ic='commit --interactive'    #was hg record
hg_d='diff --nodates'
hg_dd='diff -Bbw'
hg_dprev='diff -r .^1'
hg_l='log'
hg_a='add'
hg_r='rm'
hg_s='status'
hg_s_pipe='&& (hg resolve -l | sed -e "s/^R /OK /" )'
hg_n='identify -n -i -b -t' #hg branch ; hg log -l 1 --template "{rev}\n";
hg_n_pipe='; hg showconfig | grep paths.default='
hg_io="in ; echo ..out: ; hg out $hg_s_pipe ; hg $hg_s"
hg_oi="$hg_io"
hg_v='revert'
hg_m='merge'
hg_hs='shelve'
hg_hu='unshelve'

# git config --get remote.origin.url
git_n='remote -v'
git_n_pipe='; git branch'
#git_n_pipe='; git ls-remote --heads'
#git_n='ls-remote'
#git_n='config -l'   # config --get remote.origin.url
git_s='status -s'
git_d='diff'
git_dd='diff -b'
git_dprev='diff -r @{1}'
git_u='pull'
git_i='commit'
git_i_pipe='; git push'
git_il='commit'  #local
git_ii='add'
git_a='add'
git_l='log --name-status'
git_r='rm'
git_v='checkout --'
git_m='merge' #?
git_p='push' #?
git_hs='stash'
git_hu='stash pop'
git_io='log --branches --not --remotes ; git log --remotes --not --branches '   #??

#to turn checkout into bare:
#git config --bool core.bare true
#rm * but .git/

#to make local-dir repo shareable:
#git init --shared=0777 --bare
#chmod a+rw -R .git/
#chgrp -R somegroup .git/
#chmod g+s `find .git -type d`

####################
cmd_interactives=",i,ic,"
#cmd_interactives="$cmd_interactives,ia,"   example

test -e $0.override && . $0.override

if [ $cmd == 'v' ] ; then
	read -p "$* - REVERT - sure ?" -n 1 && echo
	if [ "$REPLY" != "y" ] ; then
		echo 'aborted'
		exit -1
	fi
fi


x=${what}_$cmd
a=${what}_${cmd}_args

#comment this out if not needed & piping break external colorizing wrappers
p=${what}_${cmd}_pipe

#if [ $x == 'hg_n' ] ; then
#fi

#only if stdout=1 is terminal and not in commit/interactive
test -z "$NOCOLOR" -a -t 1 -a "${cmd_interactives/,$cmd,/}" == "$cmd_interactives" && clrvcs=`which colorvcs.py`
CMD="$what ${!x} ${!a} "'"$@"'" ${!p}"
if test -n "$clrvcs"; then  #-a ($cmd == 'u' -o $cmd == 's')
 #for all cmds or only for upd and stat??
 test $cmd = d -o $cmd = dd -o $cmd = dprev && what=diffU
 CMD="( $CMD ) 2>&1 | $clrvcs $what 2>&1"
fi
#set -x
$E bash -o pipefail -c "$CMD" anything_as_argv0 "$@"

# vim:ts=4:sw=4:expandtab
