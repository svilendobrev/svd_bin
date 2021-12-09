ROOT ?= ./
WILD ?= *
ROOTWILD=$(ROOT)$(WILD)

all: last
	@echo i6c ? ren6v ? dt2mkv ? datev ? opt ? optjpg ? autorot ?autodate

i: i6c
v: v6c

PATH_NO_CURDIR = PATH=$${PATH\#.:} PATH=$${PATH/:.:/:}

BIN = $(dir $(MAKEFILE_LIST))

i3c 300: ren3
	$(MAKE) -f $(MAKEFILE_LIST) images
i6c 600: ren6
	$(MAKE) -f $(MAKEFILE_LIST) images v2d
pana lumix panasonic: renpana
	$(MAKE) -f $(MAKEFILE_LIST) images v2d
i530c 530 i53 53 5: ren530
	$(MAKE) -f $(MAKEFILE_LIST) images v2d
#i50c i50 50: ren50
#	$(MAKE) -f $(MAKEFILE_LIST) images
ins isn: renns
	$(MAKE) -f $(MAKEFILE_LIST) images v2d
ina ian: renna
	$(MAKE) -f $(MAKEFILE_LIST) images v2d
sony sony10 isx: rensony
	$(MAKE) -f $(MAKEFILE_LIST) images v2d

ren3:
	rename.pl 'y/A-Z/a-z/+s/img_/i3c1/' $(ROOTWILD)[jJ][pP][gG]
ren6:
	rename.pl 'y/A-Z/a-z/+s/img_/i6c2/' $(ROOTWILD)[jJ][pP][gG] $(ROOTWILD)[cC][rR]2 $(ROOTWILD)ppm
	rename.pl 'y/A-Z/a-z/+s/mvi_/v6c2/' $(ROOTWILD)[mM][oO][vV]*
	#rename.pl 'y/A-Z/a-z/+s/img_9/i6c09/+s/img_/i6c1/' $(ROOTWILD)[jJ][pP][gG]
	#rename.pl 'y/A-Z/a-z/+s/mvi_9/v6c09/+s/mvi_/v6c1/' $(ROOTWILD)[mM][oO][vV]*
ren530:
	rename.pl 'y/A-Z/a-z/+s/img_/i53c0/' $(ROOTWILD)[jJ][pP][gG]
	rename.pl 'y/A-Z/a-z/+s/mvi_/v53c0/' $(ROOTWILD)[mM][pP]4
#ren50:
#	rename.pl 'y/A-Z/a-z/+s/img_/i5c0/' $(ROOTWILD)[jJ][pP][gG]
#	rename.pl 'y/A-Z/a-z/+s/mvi_/v5c0/' $(ROOTWILD)[mM][pP]4
#	rename.pl 'y/A-Z/a-z/+s/mvi_/v5c0/' $(ROOTWILD)[mM][oO][vV]*
renpana:
	rename.pl 'y/A-Z/a-z/+s/p1240/ipan05/' $(ROOTWILD)[jJ][pP][gG]
	rename.pl 'y/A-Z/a-z/+s/p1240/vpan05/' $(ROOTWILD)[mM][pP]4*
	rename.pl 'y/A-Z/a-z/+s/p1250/ipan06/' $(ROOTWILD)[jJ][pP][gG]
	rename.pl 'y/A-Z/a-z/+s/p1250/vpan06/' $(ROOTWILD)[mM][pP]4*
	rename.pl 'y/A-Z/a-z/+s/p1260/ipan07/' $(ROOTWILD)[jJ][pP][gG]
	rename.pl 'y/A-Z/a-z/+s/p1260/vpan07/' $(ROOTWILD)[mM][pP]4*
	rename.pl 'y/A-Z/a-z/+s/p1270/ipan08/' $(ROOTWILD)[jJ][pP][gG]
	rename.pl 'y/A-Z/a-z/+s/p1270/vpan08/' $(ROOTWILD)[mM][pP]4*
	rename.pl 'y/A-Z/a-z/+s/p1280/ipan09/' $(ROOTWILD)[jJ][pP][gG]
	rename.pl 'y/A-Z/a-z/+s/p1280/vpan09/' $(ROOTWILD)[mM][pP]4*
rensn renns:
	rename.pl 'y/A-Z/a-z/+s/img_/ins_/' $(ROOTWILD)[jJ][pP][gG]
	rename.pl 'y/A-Z/a-z/+s/vid_/vns_/' $(ROOTWILD)3[gG][pP]
renan renna:
	rename.pl 'y/A-Z/a-z/+s/img_/ina_/' $(ROOTWILD)[jJ][pP][gG]
	rename.pl 'y/A-Z/a-z/+s/vid_/vna_/' $(ROOTWILD)3[gq][pP]
rensony:
	rename.pl 'y/A-Z/a-z/+s/dsc_/isx_/'  $(ROOTWILD)[jJ][pP][gG]
	rename.pl 'y/A-Z/a-z/+s,/20,/isx_20,' $(ROOTWILD)[jJ][pP][gG]
	rename.pl 'y/A-Z/a-z/+s,/20,/vsx_20,' $(ROOTWILD)[mM][pP]4*

INDEX ?= index.html
ix index: $(INDEX)
always:
%.html: always
	cd $(@D) ; pwd ; shopt -s nullglob ; AUTOSIZE=1 ~/src/bin/foto/indexer.sh $(BEFORE)$(PREDI) ./*/ *.{mkv,avi,mp4,3gp,mov} *.jpg $(AFTER)$(SLED) > $(@F)
#	cd $(@D) ; pwd ; DIRS=`ls -1d ./*/| grep -v /del` ; shopt -s nullglob ; AUTOSIZE=1 ~/src/bin/foto/indexer.sh $(BEFORE)$(PREDI) $$DIRS *.{mkv,avi,mp4,3gp,mov} *.jpg $(AFTER)$(SLED) > $(@F)
autorot:
	jhead -autorot $(ROOTWILD).jpg
autodate:
	jhead -ft $(ROOTWILD).jpg
autodaterot autorotdate:
	jhead -autorot -ft $(ROOTWILD).jpg

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

#SIZE?=1245x830
SIZE?=1536x1024
make_sz: $(OPTs:%.jpg=sz/%.jpg)
	jhead -autorot sz/*.jpg
sz/%.jpg: %.jpg
	~/src/bin/foto/fit2print.py --size=$(SIZE),pixels --djpeg --exifcopy --cjpeg=88 --autooutpfx=sz/sz $<

optjpg:
	rename.pl 's/opt$$/jpg/' $(ROOTWILD).opt

images snimki ss ii img:
	$(MAKE) -f $(MAKEFILE_LIST) j2j DEPTH=$(DEPTH)
	$(MAKE) -f $(MAKEFILE_LIST) j2j_rename DEPTH=$(DEPTH)
	$(MAKE) -f $(MAKEFILE_LIST) autodaterot

ii9: DEPTH=19
ii9: ii

DTFMT = %Y.%m.%d-%H:%M

v6 6v v6c: ren6
	$(MAKE) -f $(MAKEFILE_LIST) mov2dt
	@echo ".mov -> .mkv ; maf dt2mkv !!"
rensnv:
	rename.pl 'y/A-Z/a-z/+s/vid_/vns_/' $(ROOTWILD)3[gG][pP]*

v2d v2dt v2date vid2dt mov2dt 3gp2dt:
	shopt -s nullglob ; for a in $(ROOTWILD).{mov,3gp,mp4} ; do $E $(BIN)/vdater.py $$a ; done
dt2mkv d2v dt2v:
	-rename.py --overwrite mov.[.0-9]*.mkv mkv *.mov.*.mkv
	-rename.py --overwrite 3gp.[.0-9]*.mkv mkv *.3gp.*.mkv
	-rename.py --overwrite mp4.[.0-9]*.mkv mkv *.mp4.*.mkv
	#for a in $(ROOTWILD).dt  ; do $E $(BIN)/vdater.py $$a $${a%.dt}.mkv ; done
#	find $(ROOT) -name '$(WILD).dt' -exec bash -c "a={}"' ; $E $(BIN)/vdater.py $$a $${a%.dt}.mkv $(ARGS)' \;
#mkv4dt:
	#for a in $(ROOTWILD).mkv ; do $E $(BIN)/vdater.py $${a%.mkv}.dt $$a ; done
	#shopt -s extglob ; for a in $(ROOTWILD).mkv; do $E $(BIN)/vdater.py $${a%%?(.mov)+(.)mkv}*.dt $$a ; done
	shopt -s extglob nullglob ; for a in $(ROOTWILD).{mkv,mp4,3gp,mov}; do $E $(BIN)/vdater.py $${a%@(.mkv|.mp4|.3gp|.mov)}.dt $$a ; done
dt2avi:
	for a in $(ROOTWILD).dt  ; do $E $(BIN)/vdater.py $$a $${a%.dt}.avi ; done
avi4dt:
	for a in $(ROOTWILD).avi ; do $E $(BIN)/vdater.py $${a%.avi}.dt $$a ; done
movdate2dt:
	for a in $(ROOTWILD).mov ; do date -r $$a +$(DTFMT) > $$a.dt ; done
datev:
	for a in $(ROOTWILD).mov $(ROOTWILD).mp4 ; do touch -r $$a $$a*.mkv ; done

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

#png2jpg:
#	for a in $(ROOT)*.png; do echo "$$a" ; convert -quality 90 "$$a" "$$a.jpg" ; done
p2j png2jpg:
	find . -name \*.png -exec convert -quality 90 -verbose "{}" "{}.jpg" \;

ren-mkv-dt:
	$(PATH_NO_CURDIR) find . -name "*.mkv" -execdir rename.py --overwrite '\.[^/]*mkv$' '.mkv' {} +
	$(PATH_NO_CURDIR) find . -name "*.dt"  -execdir rename.py --overwrite '\.[^/]*dt$' '.dt' {} +
video-vse:
	find ../ -name skuka -prune -o -type f -a \( -name *.avi -o -name *.mkv -o -name *.3gp -o -name *.mp4 \) -exec ln -s {} . \;

LAST ?= 1
LAST_ONLY_FILENAME = | sed -E "s,(.*/)(.*),\2 \t: \1\2,"
last posledni:
	@find . -name i6c\*.jpg $(LAST_ONLY_FILENAME) | sort | uniq | tail -$(LAST)
	@find . -name v6c\*.mkv $(LAST_ONLY_FILENAME) | sort | uniq | tail -$(LAST)
	@find . -name i53c\*.jpg $(LAST_ONLY_FILENAME) | sort | uniq | tail -$(LAST)
	@find . -name v53c\*.mkv $(LAST_ONLY_FILENAME) | sort | uniq | tail -$(LAST)
#	@find . -name i5c\*.jpg $(LAST_ONLY_FILENAME) | sort | uniq | tail -$(LAST)
#	@find . -name v5c\*.mkv $(LAST_ONLY_FILENAME) | sort | uniq | tail -$(LAST)
	@find . -name ipan\*.jpg $(LAST_ONLY_FILENAME) | sort | uniq | tail -$(LAST)
	@find . -name vpan\*.mkv $(LAST_ONLY_FILENAME) | sort | uniq | tail -$(LAST)
	@find . -name ina\*.jpg $(LAST_ONLY_FILENAME) | sort | uniq | tail -$(LAST)
	@find . -name vna\*.[3m][gk][pv] $(LAST_ONLY_FILENAME) | sort | uniq | tail -$(LAST)
	@find . -name ins\*.jpg $(LAST_ONLY_FILENAME) | sort | uniq | tail -$(LAST)
	@find . -name vns\*.[3m][gk][pv] $(LAST_ONLY_FILENAME) | sort | uniq | tail -$(LAST)
	@find . -name isx\*.jpg $(LAST_ONLY_FILENAME) | sort | uniq | tail -$(LAST)
	@find . -name vsx\*.[3m][gkp][pv4] $(LAST_ONLY_FILENAME) | sort | uniq | tail -$(LAST)


png2pnm: $(patsubst %.png,%.pnm,$(shell find $(ROOT) $(if $(DEPTH),-maxdepth $(DEPTH)) -name '$(WILD).png'))
%.pnm: %.png
	png2pnm $< >$@

##recompress : level=medium max=95=default --method=ssim=default --accurate=no=default --subsampling=on=default
J2LEVEL=medium
J2Q=75
JARGS=
JOPTS=--quiet --accurate --no-copy
#--no-copy
Jsfx=r$(J2LEVEL)$(J2Q)
Jallsfx=jpg.r[lmhv]
DEPTH=1
JEXT=jpg
JNOLINKS = -o -type l -prune
Jall4shell = find $(ROOT) $(if $(DEPTH),-maxdepth $(DEPTH)) -name '*.$(Jallsfx)*' -prune $(JNOLINKS) -o -name '$(WILD).$(JEXT)' -print
#no symlinks

j2j: $(patsubst %,%.$(Jsfx).jpg,$(shell $(Jall4shell)))
%.$(Jsfx).jpg: % #.jpg
	-jpeg-recompress $(JOPTS) -q $(J2LEVEL)  $(if $(J2Q),--max $(J2Q)) $(if $(findstring .pnm,$<)$(findstring .ppm,$<),--ppm)  $(JARGS) "$<" "$@"
j2j_rename j2j_ren:
	$(PATH_NO_CURDIR) find $(ROOT) -name "*.$(Jsfx).jpg" -execdir rename.py --overwrite '\.jpg\.$(Jsfx)' '' {} +

jall:
	du -a -k | $(BIN)/du2sum.py kb

QIVIW=XLIB_SKIP_ARGB_VISUALS=1 qiv -l -s -m -i -f
jviw jview jqiv: WILD=*[0123456789][0123456789][0123456789]
jviw jview jqiv:
	for a in $(ROOTWILD).jpg ; do $(QIVIW) -d 1 $$a* ; done

find_cp find_and_cp:
	echo find _{FROMS} -name _{NAMEFILT} -exec cpmkdirs.sh {} _{TO} _{CPopts:--a}  \;
#2/|4/|2012/|izbor|избор
fcdir fc cmp:
	fcdir.py -t -x '/(sz/|index|del/)' $(ARGS)
apply apply-changes:
	~/src/bin/foto/apply-changes2.py --nosym -x '/([24]/|index|opis|избор|izbor|DICOM$(EXCL))' $(ARGS) $(if $Y,-y)

all_autorot all-autorot:
	$(PATH_NO_CURDIR) find . -name \*.jpg -execdir bash -c "make -f $(MAKEFILE_LIST) autorot && false " {} +
all-ix all_ix all_index ix-all:
	$(PATH_NO_CURDIR) find . -name del -prune -o -name \*.jpg -execdir bash -c "test -f index.html || make -f $(MAKEFILE_LIST) ix && false  " {} +
del-ix del_ix del_index:
	$(PATH_NO_CURDIR) find . -name index.html -delete
all_autodate all-autodate:
	$(PATH_NO_CURDIR) find . -name \*.jpg -execdir bash -c "make -f $(MAKEFILE_LIST) autodate && false " {} +
all_d2v all_dt2v all-d2v all-dt2v:
	$(PATH_NO_CURDIR) find . -name \*.dt -execdir bash -c "make -f $(MAKEFILE_LIST) d2v && false " {} +

find_sizes:
	#$(PATH_NO_CURDIR) find . -name i6\*.jpg -execdir bash -c "jhead -c {} | " +
	find . -name i6*.jpg -print0 | xargs -0 -n 100 jhead -c

vid-autorot:	#e.g. ARGS="-w 720"
	for a in $(ROOTWILD)$(EXT) ; do menc2hb "$$a" $(ARGS) ; done
vid-rot:		#e.g. EXT=sgp ROT=90
	for a in $(ROOTWILD)$(EXT) ; do menc2hb "$$a" --rotate $(ROT) $(ARGS) ; done


relink:
	shopt -s nullglob ; for x in *.jpg *.mkv; do find /snimki/ -name 2 -prune -o -type f -name "$$x" -exec ln -sfv {} . \; ; done

# vim:ts=4:sw=4:noexpandtab
