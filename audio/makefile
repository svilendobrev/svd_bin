all: mp3 flac

ifneq ($(MONO),)
OPTS+=-m m
endif
%.flac: %.wav
	flac --force -o "$@" "$<"
LAME= lame --nohist --disptime 2 -h -v -V 6 $(OPTS)

%.mp36: %.mp3
	$(LAME) "$<" "$@"
#%.mp3: %.wav
#	$(LAME) "$<" "$@"
#%.mp3: %.flac
#	flac -d "$<" -o - | $(LAME) - "$@"

%.wav: %.flac
	flac -d -o "$@" "$<"
%.wav: %.mp3
	lame --decode --nohist --quiet "$<" "$@"

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
ffres: $(patsubst %,%-$(RATE).ff.wav,$(wildcard $(INPUTS)))

%-$(RATE).sox.wav: %
	sox $<  -e signed-integer -t wav $@ $(if $(MONO),channels 1) rate -m -I -b 80 $(RATE)
soxres: $(patsubst %,%-$(RATE).sox.wav,$(wildcard $(INPUTS)))
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

ROOT=./
WAVs = $(wildcard $(ROOT)*.wav)
MP3s = $(wildcard $(ROOT)*.mp3)
FLACs = $(wildcard $(ROOT)*.flac)
flac: $(WAVs:%.wav=%.flac)
mp3 : $(WAVs:%.wav=%.mp3)
mp36: mp3mp3
mp3mp3 : $(patsubst %.mp3,%.mp36,$(wildcard $(ROOT)*.mp3))
363:
	rename.pl s/mp36/mp3/ *mp36

flacwav: $(FLACs:%.flac=%.wav)
flac2mp3: $(FLACs:%.flac=%.mp3)
mp3wav : $(MP3s:%.mp3=%.wav)
flac2wav: flacwav
mp32wav:  mp3wav
wav: $(FLACs:%.flac=%.wav) $(MP3s:%.mp3=%.wav)

#WMVs= $(wildcard *.wmv)
#wmv2mkv: $(WMVs:%.wmv=%.mkv)
wmv2mkv: $(patsubst %.wmv,%.mkv,$(wildcard *.wmv))
mkv2avi: $(patsubst %.mkv,%.avi,$(wildcard *.mkv))
avi2mkv: $(patsubst %.avi,%.mkv,$(wildcard *.avi))

wavcat:
	wavcat.py -o ooo.wav $(WAVs)

SPLIT= $(wildcard $(WILD)$(SWILD))
split: $(SPLIT:%=./mm.%-001.mkv)

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
mono2stereo.%:
	ecasound -i:"$(if $(RESAMPLE),$(_RESAMPLE))$*" -o "$@" $(_MONO2STEREO)
eca.%:
	ecasound -i:"$(if $(RESAMPLE),$(_RESAMPLE))$*" -o "$@" $(if $(PERC),-ei:$(PERC)) $(if $(MONO2STEREO)$(STEREO),$(_MONO2STEREO))

#!!без , ( ) в имената..
mono2stereo: $(patsubst %.wav,mono2stereo.%.wav,$(wildcard $(WILD)*.wav))
#	echo "$+"
eca: $(patsubst %.wav,eca.%.wav,$(wildcard $(WILD)*.wav))
#	echo "$+"
2x44: stereo-resample
stereo-resample: mono2stereo
stereo-resample: RESAMPLE=1

izv:
	$(PY) ~/src/bin/audio/izvadki/wavspl.py *izv*

FILMs= $(wildcard $(SFILM))
filmid: $(FILMs:%=%.filmid)
%.filmid: %
	filmid.sh "$<" >"$@"

bz bz2: $(patsubst %,%.bz2,$(wildcard $(BZ)))
%.bz2: %
	bzip2 $<

orgaudio:
	for a in *avi; do mkvmerge -o "$a.x.mkv" -D "$a" -A "$a...mkv"  ; done

# vim:ts=4:sw=4:noexpandtab
