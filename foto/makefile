ROOT ?= ./
WILD ?= *
ROOTWILD=$(ROOT)$(WILD)

all:
	@echo i6c ? ren6v ? datev ? opt ? optjpg ? autorot ?autodate

i: i6c
v: v6c

BIN = $(dir $(MAKEFILE_LIST))

i3c 3c c3 300: ren3
	$(MAKE) -f $(MAKEFILE_LIST) images
ren3:
	rename.pl 'y/A-Z/a-z/+s/_/1/+s/img/i3c/' $(ROOTWILD)[jJ][pP][gG]

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

SIZE?=1200x800
size: $(OPTs:%.jpg=sz/%.jpg)
sz/%.jpg: %.jpg
	~/src/bin/foto/fit2print.py --size=1200x800,pixels --djpeg --exifcopy --cjpeg=85 --autooutpfx=sz/ $<

optjpg:
	rename.pl 's/opt$$/jpg/' $(ROOTWILD).opt

600 c6 6c i6c: ren6
	$(MAKE) -f $(MAKEFILE_LIST) images
ins isn: renns
	$(MAKE) -f $(MAKEFILE_LIST) images
ina ian: renna
	$(MAKE) -f $(MAKEFILE_LIST) images
images snimki:
	$(MAKE) -f $(MAKEFILE_LIST) j2j
	$(MAKE) -f $(MAKEFILE_LIST) j2j_rename
	$(MAKE) -f $(MAKEFILE_LIST) autodate
ren6:
	rename.pl 'y/A-Z/a-z/+s/img_/i6c2/' $(ROOTWILD)[jJ][pP][gG]
	#rename.pl 'y/A-Z/a-z/+s/img_9/i6c09/+s/img_/i6c1/' $(ROOTWILD)[jJ][pP][gG]
rensn renns:
	rename.pl 'y/A-Z/a-z/+s/img_/ins_/' $(ROOTWILD)[jJ][pP][gG]
	rename.pl 'y/A-Z/a-z/+s/vid_/vns_/' $(ROOTWILD)3[gG][pP]
renan renna:
	rename.pl 'y/A-Z/a-z/+s/img_/ina_/' $(ROOTWILD)[jJ][pP][gG]
	rename.pl 'y/A-Z/a-z/+s/vid_/vna_/' $(ROOTWILD)3[gq][pP]
DTFMT = %Y.%m.%d-%H:%M

ren6v:
	rename.pl 'y/A-Z/a-z/+s/mvi_/v6c2/' $(ROOTWILD)[mM][oO][vV]*
	#rename.pl 'y/A-Z/a-z/+s/mvi_9/v6c09/+s/mvi_/v6c1/' $(ROOTWILD)[mM][oO][vV]*
v6 6v v6c:
	$(MAKE) -f $(MAKEFILE_LIST) ren6v
	$(MAKE) -f $(MAKEFILE_LIST) mov2dt
	@echo ".mov -> .mkv ; maf dt2mkv !!"
rensnv:
	rename.pl 'y/A-Z/a-z/+s/vid_/vns_/' $(ROOTWILD)3[gG][pP]*

v2dt vid2dt mov2dt 3gp2dt:
	shopt -s nullglob ; for a in $(ROOTWILD).mov $(ROOTWILD).3gp ; do $E $(BIN)/vdater.py $$a ; done
dt2mkv:
	-rename.py mov.[.0-9]*.mkv mkv *.mov.*.mkv
	-rename.py 3gp.[.0-9]*.mkv mkv *.3gp.*.mkv
	#for a in $(ROOTWILD).dt  ; do $E $(BIN)/vdater.py $$a $${a%.dt}.mkv ; done
	find $(ROOT) -name '$(WILD).dt' -exec bash -c "a={}"' ; $E $(BIN)/vdater.py $$a $${a%.dt}.mkv $(ARGS)' \;
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
	echo use: make dt2mkv
	# export TZ=EEST && for a in `find . -name \*.dt` ; do F=`dirname $$a`/`basename $$a .dt`.mkv ; test -e $$F && $$E touch -c -d `cat $$a` $$F $$a || echo $$F '??' ; done

#	find -name видео-всички -prune -o -name \*.[ma][kv][vi] -printf "%TY.%Tm.%Td-%TH:%TM %p\n"
#	#find . -name \*.mkv -print -exec date -r {} \;
optall:
	find . -type d -exec make -f $(MAKEFILE_LIST) opt -C {} \;

png2jpg:
	for a in *.png; do echo "$$a" ; convert "$$a" "$$a.jpg" ; done

ren-mkv-dt:
	PATH=$${PATH#.:} find . -name "*.mkv" -execdir rename.py  '\.[^/]*mkv$' '.mkv' {} +
	PATH=$${PATH#.:} find . -name "*.dt"  -execdir rename.py  '\.[^/]*dt$' '.dt' {} +
video-vse:
	find ../ -name skuka -prune -o -type f -a \( -name *.avi -o -name *.mkv -o -name *.3gp \) -exec ln -s {} . \;

last posledni:
	find . -name i6c\*.jpg | sed s,.*/,, | sort | tail -3
	find . -name v6c\*.mkv | sed s,.*/,, | sort | tail -3

png2pnm: $(patsubst %.png,%.pnm,$(shell find $(ROOT) $(if $(DEPTH),-maxdepth $(DEPTH)) -name '$(WILD).png'))
%.pnm: %.png
	png2pnm $< >$@

##recompress : level=medium max=95=default --method=ssim=default --accurate=no=default --subsampling=on=default
J2LEVEL=medium
J2Q=75
JARGS=
JOPTS=--quiet
#--no-copy
Jsfx=r$(J2LEVEL)$(J2Q)
Jallsfx=jpg.r[lmhv]
DEPTH=1
JEXT=jpg
Jall4shell = find $(ROOT) $(if $(DEPTH),-maxdepth $(DEPTH)) -name '*.$(Jallsfx)*' -prune -o -type l -prune -o -name '$(WILD).$(JEXT)' -print
#no symlinks

j2j: $(patsubst %,%.$(Jsfx).jpg,$(shell $(Jall4shell)))
%.$(Jsfx).jpg: % #.jpg
	-jpeg-recompress $(JOPTS) -q $(J2LEVEL)  $(if $(J2Q),--max $(J2Q)) $(if $(findstring .pnm,$<),--ppm)  $(JARGS) $< $@
j2j_rename j2j_ren:
	PATH=$${PATH#.:} PATH=$${PATH/:.:/:} find $(ROOT) -name "*.$(Jsfx).jpg" -execdir rename.py '\.jpg\.$(Jsfx)' '' {} +

jall:
	du -a -k | $(BIN)/du2sum.py kb

QIVIW=XLIB_SKIP_ARGB_VISUALS=1 qiv -l -s -m -i -f
jviw jview jqiv: WILD=*[0123456789][0123456789][0123456789]
jviw jview jqiv:
	for a in $(ROOTWILD).jpg ; do $(QIVIW) -d 1 $$a* ; done

find_cp find_and_cp:
	echo find _{FROMS} -name _{NAMEFILT} -exec cpmkdirs.sh {} _{TO} _{CPopts:--a}  \;

# vim:ts=4:sw=4:noexpandtab
