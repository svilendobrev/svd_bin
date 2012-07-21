#$Id: readme,v 1.1 2006-07-27 13:12:36 sdobrev Exp $
# most of the things below are "invented" by myself, trying, failing & man-reading.
# so, have fun. svd'99
###
#  in your .bashrc / .cshrc / .tcshrc
## setenv _INIs=path-to-these-files before sourcing these (_tcshrc/_bashrc)
## setenv _SITEs=file(s) (shell independent!) to source at the end - user/job/workplace/company dependent stuff
## setenv USER if missing
## all default to nothing

## unix does not want CRLF's - scripts, makefiles (gnumake also wants tabs), sources...
## filter before sourcing, e.g. via $(CRLF2LF) (see defalias) or unzip -a
## use makefile to generate bash's version of defalias anytime you change them
## it is possible to source filtered online with alias/function, but... too slow
# some tcsh require some-keyboard mappings to be loaded twice in order to work (e.g. UP,DOWN)

######## structure:
# _tcshrc/_bashrc:
#  -shell-dependent non-interactive (some aliases moved here!)
#    - global non-interactive  #env.rc
#   +- site-related             site.rcn
#  -shell-dependent interactive
#    - settings/init/aliases   #shname.rc 0     (before defaults)
#   +- aliases                  defalias
#   +- term detection           termname.kbd
#   +- keyboard mappings        keybinds
#    - settings/init/aliases   #shname.rc 0     (after defaults)
#   +- site-related             site.rci
# all common files shall not have if's etc; only senv, al, _set, _kxxx, so...
#
# other things to do eventualy Before this:
# - `/bin/uname` to get os-name (if there), or $OSTYPE
# - limit/u(n)limit filesize etc
# - set misc paths, e.g. MANPATH
# - use env vars to point to where some applic is on diff machines e.g. MAKE=...
# - set default permissions: umask 002      # allow group write
# - get a new beer
################
# well, as a keyboard cmdline editor tcsh is still much superior to bash;
# in bash, any aliases with arguments should be functions -- use al2func.pl
# whole .bashrc is read only for interactive scripts; use profile for non-interactive
# for fast tcsh scripts, use tcsh -f, but IMHO, better avoid programming in tcsh.
# sh functionality is MUCH better/wider

#common basic aliases/funcs expected to work
# senv          set in env
# _set          set localy
# al            alias
# so            source
# _kbin         kbd-bind builtin-command-key, e.g. delete-char
# _kcmd         kbd-bind string/command to execute immediately
# _kstr         kbd-bind string
# _setcdpath  #now commented
# verbose/unverbose     show cmds prior to expanding/exec
#
## extensibility:
# -elxxx stuff is not well tuned to this yet
# -bash's .inputrc has some interesting commands, e.g. show-all-if-ambiguous,
#   bell-style, completition-query-items, and something new about TAB:
#   menu-something - walking-through-list, as in 4dos (see tcsh's completion)
# -add other term's
# -change the aliases/kbd-mappings/whatever
# -try from scratch. may even try to incorporate 4dos aliases as well
# +send me a beer ;-)

# vim:ts=4:sw=4:expandtab
