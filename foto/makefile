ROOT ?= ./

all:
	@echo i6c ? ren6v ? datev ? opt ? optjpg ? autorot ?autodate

BIN = $(dir $(MAKEFILE_LIST))

i3c 3c c3 300: ren3
	$(MAKE) -f $(MAKEFILE_LIST) opt
ren3:
	rename.pl 'y/A-Z/a-z/+s/_/1/' $(ROOT)*JPG $(ROOT)*jpg

ix index:
	~/src/bin/foto/indexer.sh *.jpg > index.html
autorot:
	jhead -autorot $(ROOT)*.jpg
autodate:
	jhead -ft $(ROOT)*.jpg

OPTs=$(wildcard $(ROOT)*.jpg)
OPTes=$(wildcard $(ROOT)*.jpeg)
OPTs1=$(wildcard $(ROOT)*.JPG)

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

OPT2s=$(wildcard $(ROOT)*.opt)
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
	rename.pl 's/opt$$/jpg/' $(ROOT)*.opt

600 c6 6c i6c: ren6
	$(MAKE) -f $(MAKEFILE_LIST) opt
	$(MAKE) -f $(MAKEFILE_LIST) optjpg
	$(MAKE) -f $(MAKEFILE_LIST) autodate
ren6:
	rename.pl 'y/A-Z/a-z/+s/img_9/i6c09/+s/img_/i6c1/' $(ROOT)*.JPG $(ROOT)*.jpg
DTFMT = %Y.%m.%d-%H:%M

ren6v:
	rename.pl 'y/A-Z/a-z/+s/mvi_9/v6c09/+s/mvi_/v6c1/' $(ROOT)*.MOV* $(ROOT)*.mov*
v6 6v v6c:
	$(MAKE) -f $(MAKEFILE_LIST) ren6v
	$(MAKE) -f $(MAKEFILE_LIST) mov2dt
	@echo ".mov -> .mkv ; maf dt2mkv !!"

mov2dt:
	for a in $(ROOT)*.mov ; do $E $(BIN)/vdater.py $$a $${a%.mov}.dt ; done
dt2mkv:
	rename.py mov...mkv mkv *.mov...mkv
	for a in $(ROOT)*.dt  ; do $E $(BIN)/vdater.py $$a $${a%.dt}.mkv ; done
mkv4dt:
	for a in $(ROOT)*.mkv ; do $E $(BIN)/vdater.py $${a%.mkv}.dt $$a ; done
	#shopt -s extglob ; for a in $(ROOT)*.mkv; do $E $(BIN)/vdater.py $${a%%?(.mov)+(.)mkv}*.dt $$a ; done
dt2avi:
	for a in $(ROOT)*.dt  ; do $E $(BIN)/vdater.py $$a $${a%.dt}.avi ; done
avi4dt:
	for a in $(ROOT)*.avi ; do $E $(BIN)/vdater.py $${a%.avi}.dt $$a ; done
movdate2dt:
	for a in $(ROOT)*.mov ; do date -r $$a +$(DTFMT) > $$a.dt ; done
datev:
	for a in $(ROOT)*.mov ; do touch -r $$a $$a*.mkv ; done

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

# vim:ts=4:sw=4:noexpandtab
