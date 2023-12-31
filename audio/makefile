#XXX wtf.. targets (like filenames) cannot have space AND colon, errors like:
#	missing target pattern.
#	multiple target patterns.
#	target pattern contains no `%'.
#	mixed implicit and static pattern rules.

.PHONY: mp3 flac wav

all: mp3 flac

# XXX see above - no : in filenames
#_WILDS=$(wildcard $(WILD))	#does not accept multiple patterns - *.x *.y XXX
_WILDS=$(shell shopt -s nullglob && ls -1d $(WILD) && shopt -u nullglob)

ifneq ($(MONO),)
OPTS+=-m m
endif
Q=4
LAME= lame --nohist --disptime 2 -h -v -V $(Q)  $(OPTS)
#-V 6
%.mp36: Q=6
%.mp36: %.mp3
	$(LAME) "$<" "$@"
%.mp34: Q=4
%.mp34: %.mp3
	$(LAME) "$<" "$@"
%.mp3: %.flac
	flac -s -c -d "$<" | $(LAME) - "$@"
ifeq ($(NOWAV),)
%.mp3: %.wav
	$(LAME) "$<" "$@"
endif

%.mkv: %.wmv
	ffmpeg -i "$<" "$@"
VQ=-sameq
%.avi.mkv: %.mkv
	ffmpeg -i "$<" $(VQ) -acodec copy "$@"
%.avi.mkv: %.avi
	mkvmerge $< -o $@



#XXX sox is much better quality resampler than ffmpeg
%-$(RATE).ff.wav: %
	ffmpeg -i $< -ar $(RATE) $(if $(MONO),-ac 1) $@
ffres: $(patsubst %,%-$(RATE).ff.wav,$(_WILDS)))

OUT?=FLAC
RATE?=44100
%-$(RATE).sox.$(OUT): %
	sox "$<" -b 16 -e signed-integer -t $(OUT) "$@" gain -1 $(if $(STEREO),channels 2) $(if $(MONO),channels 1) rate -m -I -b 80 $(RATE) dither -s
# explicit dither, even if sox does it automatical ; and no -G or gain -n
soxres soxresample: $(patsubst %,%-$(RATE).sox.$(OUT),$(_WILDS))

flac44: WILD=*.flac
flac44:
	+$(REMAKE) RATE=44100 WILD="$(WILD)" OUT=flac soxres
#rate
# -s: steep filter
# -M/-I/-L     Phase response = minimum/intermediate/linear
# -a           Allow aliasing/imaging above the pass-band
# -b 74-99.7   passband-width %
# -p 0-100     phase response (0 = minimum, 25 = intermediate,50 = linear, 100 = maximum
#     Quality  Bandwidth  Rej dB   Typical Use
#-q     quick     n/a    ≈30 @Fs/4     playback on ancient hardware
#-l      low      80%     100     playback on old hardware
#-m    medium     95%     100     audio playback
#-h     high      95%     125     16-bit mastering (use with dither)
#-v   very high   95%     175     24-bit mastering
#sox -V  show auto-added processing
#sox -D  no auto-dither

#$(MAKE) becomes recursive only if used directly, else prefix with +
REMAKE = $(MAKE) -f $(firstword $(MAKEFILE_LIST))
#TOWAV=$(TOWAV) WAV2FLAC=$(WAV2FLAC)

WILD?=*
WAVs = $(wildcard $(WILD).wav)
MP3s = $(wildcard $(WILD).mp3)
FLACs= $(wildcard $(WILD).flac)
ifneq ($(WAV2FLAC),)
flac: $(WAVs:%.wav=%.flac)
%.flac: %.wav
	-$E flac --no-preserve-modtime --force --keep-foreign-metadata $(ARGS) -o "$@" "$<"
outflac: $(WAVs:%.wav=%.out.flac)
%.out.flac: %.wav
	/usr/local/bin/wavres44khz.py "$<" --otype flac
else
flac outflac:
	+$(REMAKE) WAV2FLAC=1 $@ WILD="$(WILD)"
outflac2: $(FLACs:%.flac=%.out.flac)
%.out.flac: %.flac
	/usr/local/bin/wavres44khz.py "$<" --otype flac
endif

ifneq ($(TOWAV),)
wav: flacwav mp3wav #$(FLACs:%.flac=%.wav) $(MP3s:%.mp3=%.wav)

%.wav: %.flac
	flac -d --no-preserve-modtime --force -o "$@" "$<"
%.wav: %.mp3
	lame --decode --nohist --quiet "$<" "$@"
else
wav:
	$(MAKE) -f $(firstword $(MAKEFILE_LIST)) TOWAV=1 $@
endif

mp3 : $(WAVs:%.wav=%.mp3)
mp3 : $(FLACs:%.flac=%.mp3)
mp36: mp3mp36
mp3mp36 mp32mp36: $(MP3s:%.mp3=%.mp36)
mp3mp34 mp32mp34: $(MP3s:%.mp3=%.mp34)
363:
	rename.pl s/mp36/mp3/ *mp36
mp34: Q=4
mp34: mp3

flacwav: $(FLACs:%.flac=%.wav)
flac2mp3: $(FLACs:%.flac=%.mp3)
mp3wav : $(MP3s:%.mp3=%.wav)
flac2wav: flacwav
mp32wav:  mp3wav

wmv2mkv: $(patsubst %.wmv,%.mkv,$(wildcard $(WILD).wmv))
mkv2avi: $(patsubst %.mkv,%.avi,$(wildcard $(WILD).mkv))
avi2mkv: $(patsubst %.avi,%.mkv,$(wildcard $(WILD).avi))

wavcat:
	wavcat.py -o ooo.wav $(WAVs)

#EXT=mkv
split: $(_WILDS:%=./mm.%-001.mkv)

T?=0:0:20 #,0:4:30
KIND?=timestamps
#parts duration
./mm.%-001.mkv: #./%
	mkvmerge "$*" -o "mm.$*" --split $(KIND):$T

#keep parts: T=a-b,c-d  e.g. T=-b,c- removes b-c
parts: $(_WILDS:%=./pp.%)
parts: KIND=parts
./pp.%: ./mm.%-001.mkv
	mkvmerge -o "pp.$*" [ `basename mm.$* .mkv`* ]

#export MKVTOOLNIX_OPTIONS=".. .."
# mkvmerge --disable-track-statistics-tags

tags:
	for a in *tags; do sh $$a; done


%.ac3: %.wav
	aften $< $@
%.avi.wav: %.avi
	mplayer -vc null -vo null -ao pcm:fast:file="$@" "$<"
#	mp2wav $< $@

#удължаване: PERC<100.0
#скъсяване : PERC>100.0
%.pitch.wav : %.wav
	ecasound -i:"$<" -o "$@" -ei:$(PERC)
.PRECIOUS: %.pitch.wav

#RESAMPLE=1
_RESAMPLE = resample,auto,
_MONO2STEREO = -chcopy 1,2
mono2stereo.%.wav:
	ecasound -i:"$(if $(RESAMPLE),$(_RESAMPLE))$*.wav" -o "$@" $(_MONO2STEREO)
eca.%.wav:
	ecasound -i:"$(if $(RESAMPLE),$(_RESAMPLE))$*" -o "$@" $(if $(PERC),-ei:$(PERC)) $(if $(MONO2STEREO)$(STEREO),$(_MONO2STEREO))

#!!без , ( ) в имената..
mono2stereo: $(_WILDS:%=mono2stereo.%.wav)
#	echo "$+"
eca: $(WAVs:%.wav=eca.%.wav)
#	echo "$+"
2x44: stereo-resample
stereo-resample: mono2stereo
stereo-resample: RESAMPLE=1

izv:
	$(PY) ~/src/bin/audio/izvadki/wavspl.py *izv*

filmid: $(_WILDS:%=%.filmid)
%.filmid: %
	filmid.sh "$<" >"$@"

bz bz2: $(_WILDS:%=%.bz2)
%.bz2: %
	bzip2 $<

orgaudio:
	for a in *avi; do mkvmerge -o "$a.x.mkv" -D "$a" -A "$a...mkv"  ; done

%.soxcut.wav: %.wav
	sox "$<" "$@" trim =$(FROM) =$(TO)

#.raw+.cue -> wav
# $bchunk .raw .cue -w xyz

######
#generic jobs

JOBS ?= $(_WILDS)
cdjob:  WILD=*/
cdjob:  $(JOBS:%=%/cdjob)
argjob: $(JOBS:%=%.argjob)

#to use aliases:
#BASH_ENV=~/.bashrc make cdjob JOB='cmd with args...'
ifneq ($(BASH_ENV),)
SHELL=bash
export ALIASYT=1
endif

%/cdjob:
	cd "$*" && $(JOB)
%.argjob:
	$(JOB) "$*"

##########

CUE=*.[Cc][Uu][eE]
#EXT=
cuetags: cdjob
cuetags: EXT?=flac
cuetags: JOB=cuetag.sh $(CUE) *.$(EXT)
#or
cue2tags: $(_WILDS:%=%._cue)
cue2tags: EXT?=flac
%._cue: EXT?=flac
%._cue: CUEITEMS?=[0-9]
%._cue:
	cd "$*" && cuetag.sh $(CUE) $(CUEITEMS)*.$(EXT)

cuetag1: .._cue		#in current dir

renunnum:
	rename.py '^([\d.]+) *(.*)\.' '$$2.$$1.' *.flac *.wav *.mp3

#re-code whatever aac into flac of same bits/freq ; use flac44 further
%.m4a2flac: %.m4a
	ffmpeg -i $< -map 0:a:0 $@

#into 16bit wav
%.wav: %.aac
	faad $<

# vim:ts=4:sw=4:noexpandtab
