ROOT ?= ../..

lc: py.lc js.lc cs.lc

TODAY = $(shell date --rfc-3339=date)
LCOUT = tee
EXCLjs = node_modules|public|gen|1|old
EXCLjsf=
EXCLpy = ui|1|node_modules|public|swagger_client|.*migrations|old.*
EXCLpyf= try[^/]*
SKIP = grep -v ' [0-9] ' |
_SORTfile = sort -k 2
_SORTcount = sort -n
SORT = | $(_SORTfile)

PYROOT ?= .
py-linecount py.lc:
	cd $(ROOT) && wc -l `find $(PYROOT) -regextype posix-egrep -regex '.*/($(EXCLpy))/.*' -prune -o -regex '.*/($(EXCLpyf)).py' -prune -o -name \*.py -print $(SORT)` | $(SKIP) $(LCOUT) $(TODAY).pylc
js-linecount js.lc:
	cd $(ROOT) && wc -l `find ui* -regextype posix-egrep -regex '.*/($(EXCLjs))/.*' -prune -o -regex '.*/($(EXCLjsf)).js' -prune -o -name \*.js -print $(SORT)` | $(SKIP) $(LCOUT) $(TODAY).jslc
cs-linecount cs.lc:
	cd $(ROOT) && wc -l `find ui* -regextype posix-egrep -regex '.*/($(EXCLjs))/.*' -prune -o -name \*.css -print $(SORT)` | $(SKIP) $(LCOUT) $(TODAY).cslc


N = 9
WHAT = {js,py}
lc-show:
	for a in *$(WHAT)lc; do echo $$a ; sort -n $$a | tail -$N ; done

DTO ?= $(shell date -I)
DFROM ?= $(DTO)
loop-lc-d:
	echo dates: DFROM=$(DFROM) DTO=$(DTO) DSTEP=1
	echo SFROM=`date --date=$(DFROM) +%s` STO=`date --date=$(DTO) +%s`
	cp makefile makefile.sav
	for ((a=`date --date=$(DFROM) +%s`; a<=`date --date=$(DTO) +%s`; a+=86400)) ; do $E hg up -C -r "branch('default') and date('<$$a 0')" ; $E m -f makefile.sav lc TODAY=`date --date=@$$a -I` LCOUT="cat>" ; done
	hg up -C
	mv $(ROOT)/*lc .

RSTEP ?= 10
loop-lc-v:
	echo revs: RFROM=$(RFROM) RTO=$(RTO) RSTEP=$(RSTEP)
	cp makefile makefile.sav
	for ((a=$(RFROM); a<=$(RTO); a+=$(RSTEP))) ;do  hg up -r $$a ; m -f makefile.sav lc TODAY=$$a LCOUT="cat>" ; done
	hg up
	mv $(ROOT)/*lc .

lc2table:
	hg log | python ./lc2table.py *.??lc > alc.csv

# vim:ts=4:sw=4:noexpandtab
