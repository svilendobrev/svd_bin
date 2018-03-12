#XXX wtf.. targets (like filenames) cannot have space AND colon, errors like:
#	missing target pattern.
#	multiple target patterns.
#	target pattern contains no `%'.
#	mixed implicit and static pattern rules.

all: mp3 flac

_WILDS=$(wildcard $(WILD))

ifneq ($(MONO),)
OPTS+=-m m
endif
LAME= lame --nohist --disptime 2 -h -v -V 6 $(OPTS)

%.mp36: %.mp3
	$(LAME) "$<" "$@"
#%.mp3: %.wav
#	$(LAME) "$<" "$@"
%.mp3: %.flac
	flac -s -c -d "$<" | $(LAME) - "$@"

%.mkv: %.wmv
	ffmpeg -i "$<" "$@"
VQ=-sameq
%.avi: %.mkv
	ffmpeg -i "$<" $(VQ) -acodec copy "$@"
%.mkv: %.avi
	mkvmerge $< -o $@



#XXX sox is much better quality resampler than ffmpeg
%-$(RATE).ff.wav: %
	ffmpeg -i $< -ar $(RATE) $(if $(MONO),-ac 1) $@
ffres: $(patsubst %,%-$(RATE).ff.wav,$(_WILDS)))

%-$(RATE).sox.wav: %
	sox "$<" -b 16 -e signed-integer -t wav "$@" $(if $(STEREO),channels 2) $(if $(MONO),channels 1) rate -m -I -b 80 $(RATE)
soxres: $(patsubst %,%-$(RATE).sox.wav,$(_WILDS))
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

REMAKE = $(MAKE) -f $(firstword $(MAKEFILE_LIST))
#TOWAV=$(TOWAV) WAV2FLAC=$(WAV2FLAC)

ROOT=./
WILD?=*
WAVs = $(wildcard $(WILD).wav)
MP3s = $(wildcard $(WILD).mp3)
FLACs= $(wildcard $(WILD).flac)
ifneq ($(WAV2FLAC),)
flac: $(WAVs:%.wav=%.flac)
%.flac: %.wav
	flac --no-preserve-modtime --force --keep-foreign-metadata $(ARGS) -o "$@" "$<"
outflac: $(WAVs:%.wav=%.out.flac)
%.out.flac: %.wav
	/usr/local/bin/wavres44khz.py "$<" --otype flac
else
flac outflac:
	$(REMAKE) WAV2FLAC=1 $@
outflac2: $(FLACs:%.flac=%.out.flac)
%.out.flac: %.flac
	/usr/local/bin/wavres44khz.py "$<" --otype flac
endif

ifneq ($(TOWAV),)
wav: flacwav mp3wav #$(FLACs:%.flac=%.wav) $(MP3s:%.mp3=%.wav)

%.wav: %.flac
	flac -d --no-preserve-modtime --force --keep-foreign-metadata -o "$@" "$<"
%.wav: %.mp3
	lame --decode --nohist --quiet "$<" "$@"
else
wav:
	$(MAKE) -f $(firstword $(MAKEFILE_LIST)) TOWAV=1 $@
endif

mp3 : $(WAVs:%.wav=%.mp3)
mp3 : $(FLACs:%.flac=%.mp3)
mp36: mp3mp3
mp3mp3 : $(MP3s:%.mp3=%.mp36)
363:
	rename.pl s/mp36/mp3/ *mp36

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
./mm.%-001.mkv: #./%
	mkvmerge "$*" -o "mm.$*" --split timecodes:$T

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
	ecasound -i:"$(if $(RESAMPLE),$(_RESAMPLE))$*" -o "$@" $(_MONO2STEREO)
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

# vim:ts=4:sw=4:noexpandtab
