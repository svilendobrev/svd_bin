#$Id: makefile,v 1.2 2006-10-05 15:57:45 sdobrev Exp $
donothing:

#all2bash: defalias.bsh $(patsubst %.tsh,%.bsh,$(wildcard aliasi/*tsh))
%.bsh: %.tsh al2func.pl
	perl -n al2func.pl $< >$@

EXCLs= \*.zip \*.tbz
zip:
	zip -ur inialias * $(INCL) $(EXCLs:%=-x %)
tar:
	tar cjf inialias`date +%m%d`.tbz * $(INCL) $(EXCLs:%=--exclude %)

DOT=.
vimm: $(DOT)linuxterm_vimrc
$(DOT)linuxterm_vimrc: _vimrc
	perl -ne '$$off++ if (/^\"if term!=linux/); print if !$$off; $$off=0 if $$off &&/^\"endif/' $? >$@

# xtermbw->xtermcolor
# assume original terminfo dir is RO, so u cant touch things there
# 1.copy -r default terminfo from /usr/share/lib to, say, myterminfo
# 2.setenv TERMINFO to that dir in THE startup script (.xsession,
# .xinitrc, .dtprofile ...)
# compile the xtermclr using  tic  (set TERMINFO to your dir before it)
# to save space, wipe all the terminfo defs but the subdir x/
## sometimes (linux/hp), tcsh complains if it finds TERM=xtermclr as
## unrecognized and then goes dumb.
## so, u may overwrite the default xterm def in the myterminfo dir

# vim:ts=4:sw=4:noexpandtab
