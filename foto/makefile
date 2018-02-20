ROOT ?= ./
WILD ?= *
ROOTWILD=$(ROOT)$(WILD)

all:
	@echo i6c ? ren6v ? datev ? opt ? optjpg ? autorot ?autodate

BIN = $(dir $(MAKEFILE_LIST))

i3c 3c c3 300: ren3
	$(MAKE) -f $(MAKEFILE_LIST) opt
ren3:
	rename.pl 'y/A-Z/a-z/+s/_/1/' $(ROOTWILD)[jJ][pP][gG]

ix index:
	~/src/bin/foto/indexer.sh *.jpg > index.html
autorot:
	jhead -autorot $(ROOTWILD).jpg
autodate:
	jhead -ft $(ROOTWILD).jpg

OPTs=$(wildcard $(ROOTWILD).jpg)
OPTes=$(wildcard $(ROOTWILD).jpeg)
OPTs1=$(wildcard $(ROOTWILD).JPG)

jpg2opt: $(OPTs:%.jpg=%.opt) $(OPTs1:%.JPG=%.opt) $(OPTes:%.jpeg=%.opt)
opt: jpg2opt
	$(MAKE) -f $(MAKEFILE_LIST) opt1jpg

%.opt: %.jpg
	jhead "$<" | grep -i progressive || jpegtran -optimize -progressive -copy all -outfile "$@" "$<"
%.opt: %.jpeg
	jhead "$<" | grep -i progressive || jpegtran -optimize -progressive -copy all -outfile "$@" "$<"
%.opt: %.JPG
	jhead "$<" | grep -i progressive || jpegtran -optimize -progressive -copy all -outfile "$@" "$<"

#	diff -q $@ $< && rm $@ || mv -f $@ $<

OPT2s=$(wildcard $(ROOTWILD).opt)
opt1jpg: $(OPT2s:%.opt=%.opt1)
opt2jpg: $(OPT2s:%.opt=%.opt2)
opt3jpg: $(OPT2s:%.opt=%.opt3)
%.opt1: %.opt
	mv -f $< $*.jpg
%.opt2: %.opt
	cp $< $*.jpg ; rm $<

opt3: $(OPTs:%.jpg=%.opt3)
%.opt3: %.jpg
	$(BIN)/jpgoptmz1.sh $<

#AUTOROT=1
2: $(OPTs:%.jpg=2/%.jpg)
2/%.jpg: %.jpg
	-$(BIN)/2small.sh $<

#AUTOROT=1
4: $(OPTs:%.jpg=4/%.jpg)
4/%.jpg: %.jpg
	-SCALE=4 $(BIN)/2small.sh $<

optjpg:
	rename.pl 's/opt$$/jpg/' $(ROOTWILD).opt

600 c6 6c i6c: ren6
	$(MAKE) -f $(MAKEFILE_LIST) opt
	$(MAKE) -f $(MAKEFILE_LIST) optjpg
	$(MAKE) -f $(MAKEFILE_LIST) autodate
ren6:
	rename.pl 'y/A-Z/a-z/+s/img_9/i6c09/+s/img_/i6c1/' $(ROOTWILD)[jJ][pP][gG]
DTFMT = %Y.%m.%d-%H:%M

ren6v:
	rename.pl 'y/A-Z/a-z/+s/mvi_9/v6c09/+s/mvi_/v6c1/' $(ROOTWILD)[mM][oO][vV]*
v6 6v v6c:
	$(MAKE) -f $(MAKEFILE_LIST) ren6v
	$(MAKE) -f $(MAKEFILE_LIST) mov2dt
	@echo ".mov -> .mkv ; maf dt2mkv !!"

mov2dt:
	for a in $(ROOTWILD).mov ; do $E $(BIN)/vdater.py $$a $${a%.mov}.dt ; done
dt2mkv:
	rename.py mov...mkv mkv *.mov...mkv
	for a in $(ROOTWILD).dt  ; do $E $(BIN)/vdater.py $$a $${a%.dt}.mkv ; done
mkv4dt:
	for a in $(ROOTWILD).mkv ; do $E $(BIN)/vdater.py $${a%.mkv}.dt $$a ; done
	#shopt -s extglob ; for a in $(ROOTWILD).mkv; do $E $(BIN)/vdater.py $${a%%?(.mov)+(.)mkv}*.dt $$a ; done
dt2avi:
	for a in $(ROOTWILD).dt  ; do $E $(BIN)/vdater.py $$a $${a%.dt}.avi ; done
avi4dt:
	for a in $(ROOTWILD).avi ; do $E $(BIN)/vdater.py $${a%.avi}.dt $$a ; done
movdate2dt:
	for a in $(ROOTWILD).mov ; do date -r $$a +$(DTFMT) > $$a.dt ; done
datev:
	for a in $(ROOTWILD).mov ; do touch -r $$a $$a*.mkv ; done

diffix:
	diff -btw index.html .. | perl -ne 'print if s/.*"(.*)".*/$$1 /' > ../rmm

view:
	qiv -s -m -i -f -d 1 *.jpg
%.ffmpeg.mkv: %.MOV
	ffmpeg -i $< -sameq $@
%.ffmpeg.mkv: %.mov
	ffmpeg -i $< -sameq $@

jpgdati:
	find . -type d -exec sh -c 'jhead -ft "{}"/*jpg' \;
videodati dati dates:
	for a in `find . -name \*.dt` ; do F=`dirname $$a`/`basename $$a .dt` ; test -e $$F && $$E touch -c -d `cat $$a` $$F $$a || echo $$F '??' ; done

#	find -name видео-всички -prune -o -name \*.[ma][kv][vi] -printf "%TY.%Tm.%Td-%TH:%TM %p\n"
#	#find . -name \*.mkv -print -exec date -r {} \;
optall:
	find . -type d -exec make -f $(MAKEFILE_LIST) opt -C {} \;

png2jpg:
	for a in *.png; do echo "$$a" ; convert "$$a" "$$a.jpg" ; done

ren-mkv-dt:
	PATH=${PATH#.:} find . -name *.mkv -execdir rename.py  '\.[^/]*mkv$' '.mkv' {} +
	PATH=${PATH#.:} find . -name *.dt  -execdir rename.py  '\.[^/]*dt$' '.dt' {} +
video-vse:
	find ../ -name skuka -prune -o -type f -a \( -name *.avi -o -name *.mkv -o -name *.3gp \) -exec ln -s {} . \;

last posledni:
	find /snimki/ -name i6c\*.jpg | sed s,.*/,, | sort | tail -5
	find /snimki/ -name v6c\*.mkv | sed s,.*/,, | sort | tail -5

##recompress : level=medium max=95=default --method=ssim=default --accurate=no=default --subsampling=on=default
J2LEVEL=medium
J2Q=95
JARGS=
JOPTS=--quiet
#--no-copy
Jsfx=r$(J2LEVEL)$(J2Q)
Jallsfx=jpg.r[lmhv]
DEPTH=15
Jall4shell = find $(ROOT) $(if $(DEPTH),-maxdepth $(DEPTH)) -name '*.$(Jallsfx)*' -prune -o -type l -prune -o -name '$(WILD).jpg' -print
#no symlinks

j2j: $(patsubst %,%.$(Jsfx).jpg,$(shell $(Jall4shell)))
%.$(Jsfx).jpg: % #.jpg
	-jpeg-recompress $(JOPTS) -q $(J2LEVEL)  $(if $(J2Q),--max $(J2Q))  $(JARGS) $< $@

#JQs={medium,high}{70,75,80,85,90,95,""}
#use OUT= for no redirect2file
#OUT = >j2jstat
#.PHONY: jall j2jstat
#j2jstat:	#no ROOT here XXX ! use make -C theroot  jstat
#	-@for lq in $(JQs) ; do X=`LANG=C du -k --total *.r$$lq.* 2>/dev/null | grep "^[1-9][0-9]*[[:space:]]*total"` && echo "$$lq: $$X" ; done $(OUT)
#	-@LANG=C du -k --total $(WILD).jpg --exclude '*$(Jallsfx)*' 2>/dev/null | grep total $(if $(OUT),>$(OUT))
#jstatall:
#	find . -depth -type d -exec $(MAKE) -f $(MAKEFILE_LIST) -C "{}" j2jstat \; #>/dev/null
#	find . -name j2jstat -print -a -exec cat {} \; >jstatall
#jall: jstatall
#	-@for lq in $(JQs); do echo $$lq: `perl -ne "print if s/$$lq: (\d+).*/\1/" jstatall | sum.py | grep -v : ` ; done
#	@echo total: `perl -ne 'print if s/^(\d+).*/\1/' jstatall | sum.py | grep -v :`

jall:
	du -a -k | $(BIN)/du2sum.py k

QIVIW=XLIB_SKIP_ARGB_VISUALS=1 qiv -l -s -m -i -f
jviw jview jqiv: WILD=*[0123456789][0123456789][0123456789]
jviw jview jqiv:
	for a in $(ROOTWILD).jpg ; do $(QIVIW) -d 1 $$a* ; done

# vim:ts=4:sw=4:noexpandtab
