IN= $(wildcard *.vob)
O=x

dai: asp deint asp2
#60
#	$(MAKE) 60

#само аспекта
asp: $(IN:%=$O.asp/%)
deint: $(IN:%=$O.deint/%)
asp2: $(IN:%=$O.asp2/%)

$O.deint/%.vob: %.vob
	mkdir -p `dirname $@`
	ffmpeg -i $< -aspect 16:9 -deinterlace -target pal-dvd $@

$O.asp2/%.vob: %.vob
	mkdir -p `dirname $@`
	ffmpeg -i $< -aspect 16:9 -target pal-dvd $@

$O.asp/%.vob: %.vob
	mkdir -p `dirname $@`
	-mpgcat -A3  $< > $@

cut 60: $(patsubst %,%/60.vob,$(wildcard $O.*))

#числата нямат нищо общо с минути/сек... нагодиго
$O.asp/60.vob: $O.asp/Video01-60.vob
	mpgcat -A3 $<  [-0:153:0] >$@
$O.asp2/60.vob: $O.asp2/Video01-60.vob makefile
	mpgcat -A3 $<  [-0:7:30] >$@
$O.deint/60.vob: $O.deint/Video01-60.vob makefile
	mpgcat -A3 $<  [-0:7:40] >$@

60-vob:
	rename.pl s/60/Video01-60/ x.*/60.vob

#   VRATE=6000 IN=koleduvane-sladkavoda-12.2011-otkys.raw.avi OUT=kkk.avi PASS1=0  menc1 -aspect 16:9 -vf scale -zoom -xy 640
otkys:
	VRATE=6000 IN=koleduvane-sladkavoda-12.2011-otkys.raw.avi OUT=kkk.avi   menc1 -aspect 16:9 -vf scale -zoom -xy 640

M=km.mpg

dvd2mpg: $M
$M:
	mplayer -dumpstream -dumpfile $@ -dvd-device /media/tmp/ dvd://1 $(ARG)
$M.asp.mpg: $M
	mpgcat -A3 $<  >$@
asp.otpred $M.otpred.mpg: $M
	mpgcat -A3 $< [0:2:30-] >$M.otpred.mpg
asp.otzad: $M.otpred.mpg
	mpgcat -A3 $< [-0:206:50] >$M.otpred.otzad.mpg

HAND = handbrake-cli -i $< -e x264 -2 -T --vfr -q 20 -o $@ --crop 4:4:0:0 $(if $W,-w) $W $(ARGS)
N= km.mpg.asp.mpg

#W=480
#CUTS=--start-at sec:23 --stop-at sec:400
decomb.%: ARGS=--decomb
deint.%: ARGS=--deinterlace

%.mkv: $N
	$(HAND) $(CUTS)

%.mp4: W=480
%.mp4: $N
	$(HAND) $(CUTS)
%.decomb.mp4: $N
	$(HAND) $(CUTS) --decomb
%.deint.mp4: $N
	$(HAND) $(CUTS) --deinterlace

pred.%.mkv: %.mkv
	aaa

#SWILD=...
T?=0:0:23
otpred:
	$(MAKE) -f ~/src/bin/audiovideo/makefile split
#mm.%-001.mkv: %
#	mkvmerge $< -o mm.$* --split timecodes:$T

# vim:ts=4:sw=4:noexpandtab
